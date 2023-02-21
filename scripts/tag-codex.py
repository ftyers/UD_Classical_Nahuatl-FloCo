import sys, re

alphabet = 'abcdefghijklmnopqrstuvxyz'

def guess(norm):
	if re.findall('[aeiou]tl$', norm):
		return ('NOUN', '_', 'Guessed=Yes')
	if re.findall('[aeiouv][^aeiou]+tli$', norm):
		return ('NOUN', '_', 'Guessed=Yes')
	if re.findall('[a-z]+yotl$', norm):
		return ('NOUN', '_', 'Guessed=Yes')
	if re.findall('[a-z]+huitl$', norm):
		return ('NOUN', '_', 'Guessed=Yes')
	if re.findall('[a-z]+catl$', norm):
		return ('NOUN', '_', 'Guessed=Yes')
	if re.findall('[a-z]+iztli$', norm):
		return ('NOUN', '_', 'Guessed=Yes')
	if re.findall('[a-z]+huilia$', norm):
		return ('VERB', '_', 'Guessed=Yes')
	if re.findall('[a-z]+ltia$', norm):
		return ('VERB', '_', 'Guessed=Yes')
	if re.findall('^qui[a-z]+([io]|hu)a$', norm):
		return ('VERB', '_', 'Guessed=Yes')
	if re.findall('^mo[a-z]+lia$', norm):
		return ('VERB', '_', 'Guessed=Yes')
	if re.findall('^[a-z]+zque$', norm):
		return ('VERB', '_', 'Guessed=Yes')
	return ('X', '_', '_')

def tag(lexicon, form, norm, idx):
	lower = norm.lower()
	if lower in lexicon:
		return (lexicon[lower][0], lexicon[lower][1], '_')
	if norm[0] in '0123456789':
		return ('NUM', '_', '_')
	if norm[0].upper() == norm[0] and idx > 1 and norm[0].lower() in alphabet:
		return ('PROPN', '_', '_')
	if norm[0] in '.?!:,;':
		return ('PUNCT', '_', '_')

	return guess(norm)

def read_lexicon(fn):
	lexicon = {}
	for line in open(fn).readlines():
		if line[0] == '#':
			continue
		tag, feats, token = line.strip().split('\t')
		if token in lexicon:
			lexicon[token] = (lexicon[token][0] + '|' + tag, '_')
		else:
			lexicon[token] = (tag, feats)
	return lexicon
		
lexicon = read_lexicon('lexicon.tsv')

total = 0
tagged = 0

for bloc in sys.stdin.read().split('\n\n'):
	bloc = bloc.strip()

	if not bloc: 
		continue

	comments = [line for line in bloc.split('\n') if line and line[0] == '#']
	lines = [line for line in bloc.split('\n') if line and line[0] != '#']
	new_lines = []
	n_tokens = 0
	n_tagged = 0

	for line in lines:
		# ID · FORM · LEMMA · UPOS · XPOS · FEATS · HEAD · DEPREL · EDEPS · MISC
		# 0    1      2       3      4      5       6      7        8       9
		row = line.split('\t')
			
		idx = int(row[0])
		form = row[1]
		misc = row[9]
		attrs = {pair.split('=')[0] : pair.split('=')[1] for pair in misc.split('|')}
		norm = attrs['Norm']

		upos, ufeats, addmisc = tag(lexicon, form, norm, idx)
		row[3] = upos
		row[5] = ufeats
		if addmisc != '_':
			row[9] = row[9] + '|' + addmisc

		if upos != 'X':
			tagged += 1
			n_tagged += 1
		total += 1
		n_tokens += 1

		#print('\t'.join(row))
		new_lines.append(row)

	print('\n'.join(comments))
	if n_tokens > 0:
		print('# tagged = %.2f%%' % (n_tagged/n_tokens*100))
	for row in new_lines:
		print('\t'.join(row))
	

	print()

if total != 0:
	print('%.2f%%' % (tagged/total*100),file=sys.stderr)
