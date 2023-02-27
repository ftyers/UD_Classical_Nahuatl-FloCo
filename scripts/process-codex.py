import sys, re, os
from Trie import PrefixTree

def tokenise(s):
	o = s
	o = re.sub('([,:.;?!]+)', ' \g<1> ', o)
	for etc in ['etc', '&c', 'Etc', 'q. n']:
		o = o.replace(etc + ' .', etc + '.')
		o = o.replace('. ' + etc, etc)
	o = re.sub('  *', ' ', o)
	o = o.strip()
	return o.split(' ')

def detokenise(s):
	o = s
	o = re.sub(' ([,:.;?!]+) ', '\g<1> ', o)
	o = re.sub(' ([,:.;?!]+)$', '\g<1>', o)
	return o

def normalise(table, overrides, s, idx):
#	print('@',idx, s, overrides, file=sys.stderr)
	s = s.strip('¶')
	if idx in overrides:
		form = overrides[idx][1]
		return form, form, table[0][s.lower()][1]
	if s in table[0]:
		form = table[0][s][0]
		return form, form, table[0][s][1]
	if s[0].isupper() and s.lower() in table[0]:
		form = table[0][s.lower()][0].title()
		return form, form, table[0][s.lower()][1]
	if s[0] in ',:.;?!':
		return s, s, False

	return '*'+s, s, False 

def maxmatch(tree, sentence):
#	token += ' '

	if len(sentence) == 0:
		return []

	for i in range(1, len(sentence)):
		firstSpan = sentence[0:-i]
		remainder = sentence[-i:]
#		print('@', firstSpan[0][0], firstSpan)
		found = tree.find_span(firstSpan)
		if found:
#			print('fw:',firstSpan)	
			return [{'repl': found.replacement, 'span':firstSpan}] + maxmatch(tree, remainder)

	firstSpan = sentence[0]
	remainder = sentence[1:]

	return [firstSpan] + maxmatch(tree, remainder)


def retokenise(tree, sentence):
	spans = maxmatch(tree, sentence)
	return spans
	
def load_tree(fn):
	tree = PrefixTree()
	for line in open(fn):
		if line[0] == '#' or line.strip() == '':
			continue
		left, right = line.strip().split('\t')
		span = left.split(' ')
		tree.insert(span, right)	
	return tree

def load_normalisation_table(fn):
	table = {}
	lineno = 0
	for lineno, line in enumerate(open(fn)):
		if line.strip() == '' or line[0] == '#':
			continue
		try:
			line = re.sub('\t\t*', '\t', line)
			level, left, right = line.strip().split('\t')
		except:
			print('!!! Error wrong number of values in line %d' % lineno, file=sys.stderr)
			print('!!!', line, file=sys.stderr)
			raise
			
		level = int(level)
		if level not in table:
			table[level] = {}
		if left not in table[level]:
			table[level][left] = {}
		if len(table[level][left]) > 0: # ambiguous
			table[level][left] = (table[level][left][0] + '/' + right, True)
		else:
			table[level][left] = (right, False)
	return table

def load_override_table(fn):
	table = {}
	for line in open(fn):
		sent_id, token_id, left, right = line.strip().split('\t')
		token_id = int(token_id)
		if sent_id not in table:
			table[sent_id] = {}
		if token_id not in table[sent_id]:
			table[sent_id][token_id] = {}
		# left here is only for sanity checking
		table[sent_id][token_id] = (left, right)
	return table
		
tree = load_tree('retokenisation.tsv')
table = load_normalisation_table('normalisation.tsv')
overrides = load_override_table('overrides.tsv')

#print(tree.size())
#tree.display()
current_token = ''
current_line = 0
current_folio = 'UND'
current_paragraph = 0
book = os.path.basename(sys.argv[1])
tokens = []


for line in open(sys.argv[1]):
	if re.findall(' [Ff]ol?. *[0-9]+', line):
		current_folio = re.sub('[^0-9]+', '', line.replace('fo.','').strip())
		current_paragraph = 0
		current_line = 0
		continue

	line = line.strip() + '¶'
	line = re.sub('\([0-9]+\)', '', line)
	# We need to track and replace tokens that end in a full stop
	line = line.replace('q. n.', '@#@16@#@ @#@17@#@')

	if line.strip() == '¶':
		current_paragraph += 1
		current_line = 1
		continue

	for token in tokenise(line):
		tokens.append((token, current_folio, current_paragraph, current_line))

	current_line += 1

current_sentence_id = 1
current_sentence = []
norm_overrides = {}
for token in tokens:
	if token[0] != '¶':
		# Make this more beautiful
		if token[0] in ['@#@16@#@', '@#@17@#@']:
			if token[0] == '@#@16@#@':
				current_sentence.append(('q.', token[1], token[2], token[3]))
				continue
			if token[0] == '@#@17@#@':
				current_sentence.append(('n.', token[1], token[2], token[3]))
				continue
		else: 
			current_sentence.append(token)
	if token[0] == '.' or token[0] == '?' or token[0].lower() in ['&c.', 'etc.']:
		sentence = '·'.join([token[0] for token in current_sentence])
		sentence = sentence.replace('¶·', '¶')

		s2 = retokenise(tree, current_sentence)

		sentence_id_string = '%s:%d' % (book, current_sentence_id)
		if sentence_id_string in overrides:
			norm_overrides = overrides[sentence_id_string]
		else:
			norm_overrides = {}

		idx = 1
		lines = []
		retokenised_sentence = []
		normalised_sentence = []
		for i, token in enumerate(s2):
			if type(token) == type({}):
				subtokens = token['repl'].split('·')
				for subtoken in subtokens:	
					manu = '·'.join([i[0] for i in token['span']])
					foli = ','.join([i[1] for i in token['span']])
					para = ','.join(['%d' % i[2] for i in token['span']])
					line = ','.join(['%d' % i[3] for i in token['span']])
					norm, norm_form, ambiguous = normalise(table, norm_overrides, subtoken, idx)
					if ambiguous:
						lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s|AmbigNorm=%s' % (manu, foli, para, line, norm, ambiguous)))
					else:
						lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s' % (manu, foli, para, line, norm)))
					idx += 1
					retokenised_sentence.append(subtoken.strip('¶'))
					normalised_sentence.append(norm_form.replace('*', ''))
			else:
				form = token[0].strip('¶')
				norm, norm_form, ambiguous = normalise(table, norm_overrides, token[0], idx)
				if ambiguous:
					lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, form, '_', '_', '_', '_', '_', '_', '_', 'Folio=%s|Paragraph=%d|Line=%d|Norm=%s|AmbigNorm=%s' % (token[1], token[2], token[3], norm, ambiguous)))
				else:
					lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, form, '_', '_', '_', '_', '_', '_', '_', 'Folio=%s|Paragraph=%d|Line=%d|Norm=%s' % (token[1], token[2], token[3], norm)))
				retokenised_sentence.append(form.strip('¶'))
				normalised_sentence.append(norm_form.replace('*', ''))
				idx += 1

		print('# sent_id = %s:%d' % (book, current_sentence_id))
		print('# text = %s' % detokenise(' '.join(retokenised_sentence)))
		print('# text[norm] = %s' % detokenise(' '.join(normalised_sentence)))
		print('# text[orig] = %s' % detokenise(sentence))
		for line in lines:
			print(line)
		print()
		current_sentence = []
		current_sentence_id += 1
		
