import sys, re, os
from Trie import PrefixTree

def tokenise(s):
	o = s
	o = re.sub('([,:.;?!]+)', ' \g<1> ', o)
#	o = o.replace('etc .', 'etc.')
#	o = o.replace('Etc .', 'Etc.')
	o = re.sub('  *', ' ', o)
	o = o.strip()
	return o.split(' ')

def detokenise(s):
	o = s
	o = re.sub(' ([,:.;?!]+) ', '\g<1> ', o)
	o = re.sub(' ([,:.;?!]+)$', '\g<1>', o)
	return o

def normalise(table, s, idx):
#	print(idx, s, file=sys.stderr)
	s = s.strip('¶')
	if s in table[0]:
		return table[0][s]
	if s[0].isupper() and s.lower() in table[0]:
		return table[0][s.lower()].title()

	return s	

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
		left, right = line.strip().split('\t')
		span = left.split(' ')
		tree.insert(span, right)	
	return tree

def load_table(fn):
	table = {}
	for line in open(fn):
		level, left, right = line.strip().split('\t')
		level = int(level)
		if level not in table:
			table[level] = {}
		if left not in table[level]:
			table[left] = {}
		table[level][left] = right
	return table
		
tree = load_tree('retokenisation.tsv')
table = load_table('normalisation.tsv')

#print(tree.size())
#tree.display()
current_token = ''
current_line = 0
current_folio = 'UND'
current_paragraph = 0
book = os.path.basename(sys.argv[1])
tokens = []


for line in open(sys.argv[1]):
	if re.findall(' fo. *[0-9]+', line):
		current_folio = line.replace('fo.','').strip()
		current_paragraph = 0
		current_line = 0
		continue

	line = line.strip() + '¶'
	line = re.sub('\([0-9]+\)', '', line)

	if line.strip() == '¶':
		current_paragraph += 1
		current_line = 1
		continue

	for token in tokenise(line):
		tokens.append((token, current_folio, current_paragraph, current_line))

	current_line += 1

current_sentence_id = 1
current_sentence = []
for token in tokens:
	if token[0] != '¶':
		current_sentence.append(token)
	if token[0] == '.' or token[0] == '?':
		sentence = '·'.join([token[0] for token in current_sentence])
		sentence = sentence.replace('¶·', '¶')

		s2 = retokenise(tree, current_sentence)

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
					norm = normalise(table, subtoken, idx)
					lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s' % (manu, foli, para, line, norm)))
					idx += 1
					retokenised_sentence.append(subtoken.strip('¶'))
					normalised_sentence.append(norm)
			else:
				form = token[0].strip('¶')
				norm = normalise(table, token[0], idx)
				lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (i+1, form, '_', '_', '_', '_', '_', '_', '_', 'Folio=%s|Paragraph=%d|Line=%d|Norm=%s' % (token[1], token[2], token[3], norm)))
				retokenised_sentence.append(form.strip('¶'))
				normalised_sentence.append(norm)
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
		



