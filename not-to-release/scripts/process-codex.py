import sys, re, os
from Trie import PrefixTree
import glob
# from ml_support import load_retokenization_model, retokenize_w_model

def tokenise(s):
	o = s
	o = re.sub('([,:.;?!()]+)', ' \g<1> ', o)
	o = o.replace(" ). ", " ) . ")
	for etc in ['etc', '&c', 'Etc', 'q. n', 'xpo', '14', 'p', 'N']:
		o = o.replace(etc + ' .', etc + '.')
		o = o.replace('. ' + etc, etc)
	o = re.sub('  *', ' ', o)
	o = o.strip()
	return o.split(' ')

def detokenise(s, manual=False):
	o = s
	if manual:
		o = o.replace('@', '')
		o = o.replace('|', '')
	o = re.sub(' ([,:.;?!]+) ', '\g<1> ', o)
	o = re.sub(' ([,:.;?!]+)$', '\g<1>', o)
	o = o.replace("( ", "(").replace(" )", ")").replace(" .)", ".)")
	return o

def normalise(table, overrides, s, idx):
#	print('@',idx, s, overrides, file=sys.stderr)
	s = s.strip('¶')
	if s == '':
		print('WARNING: Empty token:', idx, s, file=sys.stderr)

	if idx in overrides:
		form = overrides[idx][1]
		return form, form, table[0][s.lower()][1], True
	if s in table[0]:
		form = table[0][s][0]
		if table[0][s][1]:
			# We guarantee that the highest ranked is first
			form = table[0][s][0].split('/')[0]
		return form, form, table[0][s][1], False
	if s[0].isupper() and s.lower() in table[0]:
		form = table[0][s.lower()][0].title()
		return form, form, table[0][s.lower()][1], False
	if s[0] in ',:.;?!()':
		return s, s, False, False
	num = True
	for c in s:
		if c not in '1234567890':
			num = False
	if num:
		return s, s, False, False

	return '*'+s, s, False, False

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

def retokenise(tree, sentence, model_bundle=None, manual=False):
	spans = []
	#print(sentence)
	if manual:
		"""
			When we have the tokenisation provided in the file
		"""
		def clean_repl(s):
			return s.replace('@', '').replace('|', '·').replace('¶','')
		# {'repl': 'ilhujuh', 'span': [('il¶', '19', 4, 12), ('hujuh', '19', 4, 13)]}
		# (token, current_folio, current_paragraph, current_line)
		# ('yoan', '1', 1, 4), ('i@¶', '1', 1, 4), ('n|juh', '1', 1, 5)
		buf = {'repl': '', 'span': []}
		idx = 0
		while idx < len(sentence):
			if sentence[idx][0].replace('¶','').strip()[-1] == '@':
				temp = sentence[idx][0]
				temp = temp.replace('@', '').replace('|', '·')
				sentence[idx] = (temp, sentence[idx][1], sentence[idx][2], sentence[idx][3])
				buf['repl'] += sentence[idx][0]
				buf['span'].append(sentence[idx])
			else:
				if buf['repl'] != '':
					temp = sentence[idx][0]
					temp = temp.replace('@', '').replace('|', '·')
					sentence[idx] = (temp, sentence[idx][1], sentence[idx][2], sentence[idx][3])
					buf['repl'] += sentence[idx][0]
					buf['span'].append(sentence[idx])
					buf['repl'] = clean_repl(buf['repl'])
					spans.append(buf)
					buf = {'repl': '', 'span': []}
				else:
					if '|' in sentence[idx][0]:
						buf = {'repl': '', 'span': []}
						temp = sentence[idx][0]
						temp = temp.replace('@', '').replace('|', '·')
						sentence[idx] = (temp, sentence[idx][1], sentence[idx][2], sentence[idx][3])
						buf['repl'] += sentence[idx][0]
						buf['span'].append(sentence[idx])
						buf['repl'] = clean_repl(buf['repl'])
						spans.append(buf)
						buf = {'repl': '', 'span': []}
					else:
						spans.append(sentence[idx])
			idx += 1
	else:
		spans = maxmatch(tree, sentence)

	#print(spans)

	# if model_bundle is not None:
	# 	sentence = (
	# 		"·".join([t[0] for t in sentence]).replace("¶·", "¶")
	# 	)
	# 	spans = retokenize_w_model(
	# 		spans, sentence, model_bundle["vectorizer"], model_bundle["model"], threshold=0.5
	# 	)
	return spans
	
def load_tree(fn, tree):
	for lineno, line in enumerate(open(fn)):
		if line[0] == '#' or line.strip() == '':
			continue
		try:
			left, right = line.strip().split('\t')
		except:
			print('!!! Error wrong number of values in line %d' % lineno, file=sys.stderr)
		span = left.split(' ')
		tree.insert(span, right)	
	return tree

def load_normalisation_table(fn, table):
#	table = {}
	lineno = 0
	ranks = {}
	for lineno, line in enumerate(open(fn)):
		if line.strip() == '' or line[0] == '#':
			continue
		try:
			line = re.sub('\t\t*', '\t', line)
			level, rank, left, right = line.strip().split('\t')
		except:
			print('!!! Error wrong number of values in line %d' % lineno, file=sys.stderr)
			print('!!!', line, file=sys.stderr)
			continue
			#raise
			
		level = int(level)
		rank = int(rank)
		if left not in ranks:
			ranks[left] = []
		ranks[left].append((rank, right))
		if level not in table:
			table[level] = {}
		if left not in table[level]:
			table[level][left] = {}
		if len(table[level][left]) > 0: # ambiguous
			ranks[left] = list(set(ranks[left]))
			ranks[left].sort()
			table[level][left] = ('/'.join([j for i,j in ranks[left]]), True)
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

def load_subtoken_table(fn):
	table = {}
	for line in open(fn):
		if line[0] == '#':
			continue
		token, subtokens, sent_ids = re.sub('\t\t*', '\t', line).strip().split('\t')
		token = token.strip()
		subtokens = subtokens.split('|')
		sent_ids = sent_ids.split(' ')
		if token not in table:
			table[token] = {}
		for sent_id in sent_ids:
			table[token][sent_id] = subtokens

	return table
		
tree = PrefixTree()
tree = load_tree('retokenisation.tsv', tree)
for fn in glob.glob('retokenisation/*.retok'):
	tree = load_tree(fn, tree)
#
# Use a statistical model to retokenize after running rules:
#
# retokenization_bundle = load_retokenization_model()

table = load_normalisation_table('normalisation.tsv', {})
for fn in glob.glob('normalisation/*.norm'):
	table = load_normalisation_table(fn, table)
	
overrides = load_override_table('overrides.tsv')
subtoken_table = load_subtoken_table('subtokens.tsv')

#print(tree.size())
#tree.display()
current_token = ''
current_line = 0
current_folio = 'UND'
current_paragraph = 0
book = os.path.basename(sys.argv[1])
tokens = []

manual_tokenisation = False

book_text = re.sub('  *', ' ', open(sys.argv[1]).read())
if '@' in book_text:
	book_text = re.sub(' *@ *', '@ ', book_text)
	book_text = re.sub(' *\n@', '@\n', book_text)
	# '|' followed by a space is a mistake
	# Auh intlacamo motlapaloa
	# pilhoaque, in quj@chioaz in, ticitl:
	# nj@man vel qujtzatzaqua in cioatzin@
	# tli. A@uh in@tla|ic| mjquj ijti, mj@
	# toa, motocaiotia: mocioaque@
	book_text = re.sub('\| ', ' ', book_text) 
	# In iehoantin,|y, moteneoa tlalo
	book_text = re.sub(',\|', ', ', book_text) 
	book_text = re.sub('\.\|', '. ', book_text) 
	manual_tokenisation = True

lines = re.sub('  *', ' ', book_text).split('\n')

for line in lines:
	if re.findall(' [Ff]ol?. *[0-9]+', line):
		current_folio = re.sub('[^0-9]+', '', line.replace('fo.','').strip())
		current_paragraph = 0
		current_line = 0
		continue

	line = line.strip() + '¶'
	line = re.sub('\([0-9]+\)', '', line)
	# We need to track and replace tokens that end in a full stop
	line = line.replace('q. n.', '@#@16@#@ @#@17@#@')
	line = line.replace('xpo.', '@#@18@#@')
	line = line.replace('14.', '@#@19@#@')
	line = line.replace('p.', '@#@20@#@')
	line = line.replace('N.', '@#@21@#@')

	if line.strip() == '¶':
		current_paragraph += 1
		current_line = 1
		continue

	for token in tokenise(line):
		token = token.strip('^') # for inserted tokens
		tokens.append((token, current_folio, current_paragraph, current_line))

	current_line += 1

current_sentence_id = 1
current_sentence = []
norm_overrides = {}
for token in tokens:
#	print('TOKEN:', token, [i[0] for i in current_sentence])
	if token[0] != '¶':
#		print('!!!', token[0].strip('¶'))
		# Make this more beautiful
		newtok = token
		token_check = token[0].strip('¶')
		if token[0].strip('¶') in ['@#@16@#@', '@#@17@#@', '@#@18@#@', '@#@19@#@', '@#@20@#@']:
			if token_check == '@#@16@#@':
				newtok = ('q.', token[1], token[2], token[3])
			elif token_check == '@#@17@#@':
				newtok = ('n.', token[1], token[2], token[3])
			elif token_check == '@#@18@#@':
				newtok = ('xpo.', token[1], token[2], token[3])
			elif token_check == '@#@19@#@':
				newtok = ('14.', token[1], token[2], token[3])
			elif token_check == '@#@20@#@':
				newtok = ('p.', token[1], token[2], token[3])
			elif token_check == '@#@21@#@':
				newtok = ('N.', token[1], token[2], token[3])
		current_sentence.append(newtok)

	if token[0] == '.' or token[0] == '?' or token[0].lower() in ['&c.', 'etc.']:
		sentence = '·'.join([token[0] for token in current_sentence])
		sentence = sentence.replace('¶·', '¶')

		#
		# Remove model_bundle=... to revert to sans-model mode.
		#
		s2 = retokenise(tree, current_sentence, manual=manual_tokenisation)  #, model_bundle=retokenization_bundle)

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
					norm, norm_form, ambiguous, overridden = normalise(table, norm_overrides, subtoken, idx)

					conllu_subtokens = []
					if subtoken in subtoken_table:
						if sentence_id_string in subtoken_table[subtoken]:
							conllu_subtokens = subtoken_table[subtoken][sentence_id_string]

					if len(conllu_subtokens) > 0:
						span = '%d-%d' % (idx, idx+len(conllu_subtokens) -1)
						lines.append('%s\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (span, subtoken))
						for conllu_subtoken in conllu_subtokens:
							norm, norm_form, ambiguous, overridden = normalise(table, norm_overrides, conllu_subtoken, idx)
							lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, conllu_subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s' % (manu, foli, para, line, norm)))
							normalised_sentence.append(norm_form.replace('*', ''))
							idx += 1
					else:
						if ambiguous:
							lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s|AmbigNorm=%s|Override=%s' % (manu, foli, para, line, norm, ambiguous, overridden)))
						else:
							lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s' % (manu, foli, para, line, norm)))
						idx += 1
						normalised_sentence.append(norm_form.replace('*', ''))
					retokenised_sentence.append(subtoken.strip('¶'))
			else:
				form = token[0].strip('¶')
				norm, norm_form, ambiguous, overridden = normalise(table, norm_overrides, token[0], idx)

				conllu_subtokens = []
				if form in subtoken_table:
					if sentence_id_string in subtoken_table[form]:
						conllu_subtokens = subtoken_table[form][sentence_id_string]

				if len(conllu_subtokens) > 0:
					span = '%d-%d' % (idx, idx+len(conllu_subtokens) -1)
					lines.append('%s\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (span, form))
					for conllu_subtoken in conllu_subtokens:
						norm, norm_form, ambiguous, overridden = normalise(table, norm_overrides, conllu_subtoken, idx)
						lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, conllu_subtoken, '_', '_', '_', '_', '_', '_', '_', 'Orig=%s|Folio=%s|Paragraph=%s|Line=%s|Norm=%s' % (manu, foli, para, line, norm)))
						normalised_sentence.append(norm_form.replace('*', ''))
						idx += 1
				else:
					if ambiguous:
						lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, form, '_', '_', '_', '_', '_', '_', '_', 'Folio=%s|Paragraph=%d|Line=%d|Norm=%s|AmbigNorm=%s|Override=%s' % (token[1], token[2], token[3], norm, ambiguous, overridden)))
					else:
						lines.append('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (idx, form, '_', '_', '_', '_', '_', '_', '_', 'Folio=%s|Paragraph=%d|Line=%d|Norm=%s' % (token[1], token[2], token[3], norm)))
					normalised_sentence.append(norm_form.replace('*', ''))
					idx += 1
				retokenised_sentence.append(form.strip('¶'))
	
		print('# sent_id = %s:%d' % (book, current_sentence_id))
		print('# text = %s' % detokenise(' '.join(retokenised_sentence)))
		print('# text[norm] = %s' % detokenise(' '.join(normalised_sentence)))
		print('# text[orig] = %s' % detokenise(sentence, manual=manual_tokenisation))
		for line in lines:
			print(line)
		print()
		current_sentence = []
		current_sentence_id += 1
