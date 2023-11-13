import sys, glob, os, re

books = {}
translations = {}

maxlen = 0
for path in glob.glob('../conllu/*.conllu'):
	book = os.path.basename(path).replace('.conllu','')
	books[book] = {}
	translations[book] = {'Spa':0, 'Eng': 0, 'OldSpa':0, 'Nhi':0}

	if len(book) > maxlen:
		maxlen = len(book)

	trees = 0
	tokens = 0
	normalised = 0
	tagged = 0
	heads = 0
	relations = 0
	lemmatised = 0
	analysed = 0
	glosses = 0
	for bloc in open(path).read().split('\n\n'):
		for line in bloc.split('\n'):
			if line.strip() == '':
				continue
			if line[0] == '#':
				if 'text[spa]' in line:
					translations[book]['Spa'] += 1
				elif 'text[eng]' in line:
					translations[book]['Eng'] += 1
				elif 'text[nhi]' in line:
					translations[book]['Nhi'] += 1
				elif 'text[osp]' in line:
					translations[book]['OldSpa'] += 1
				continue
			row = line.split('\t')
			if '.' in row[0] or '-' in row[0]:
				continue
			if len(row) != 10:
				continue

			if len(re.findall('[^g]Norm=[^*]', row[9])) > 0:
				normalised += 1

			if row[3] != '_' and row[3] != 'X':
				tagged += 1

			if row[2] != '_':
				lemmatised += 1
	
			if 'Analysed=Yes' in row[9]:
				analysed += 1

			if 'Gloss=' in row[9]:
				glosses += 1

			# id, form, lem, upos, xpos, feat, head, dep, deps, misc
			# 0   1     2    3     4     5     6     7    8     9
			if '_' not in row[6]:
				heads += 1
			if '_' not in row[7]:
				relations += 1
	
			tokens += 1
		
		trees += 1
		
	books[book] = [trees, tokens, normalised, tagged, lemmatised, analysed, heads, relations, glosses, translations[book]]

langs = '\t'.join(translations[book].keys())
print('%s\tTrees\tTokens\tNorm\tTagged\tLemmas\tFeats\tHeads\tRels\tGloss\t%s' % (' ' * (maxlen + 2), langs))
for book in books:
	pad = ' ' * ((maxlen - len(book)) + 2)
	tokens = books[book][1]
	trees = books[book][0]
	cols = [book + pad] + books[book][:2] + ['%.2f' % ((i/tokens)*100) for i in books[book][2:-1]]
	cols2 = ['%.2f' % ((v/trees)*100) for k, v in translations[book].items()]
	#[trees, tokens, normalised, tagged, lemmatised, analysed, heads, relations, glosses] = books[book]
		

#	print(f'{book + pad}\t{trees}\t{tokens}\t{normalised}\t{tagged}\t{lemmatised}\t{analysed}\t{heads}\t{relations}\t{glosses}')
	print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t' % tuple(cols), '\t'.join(cols2))
