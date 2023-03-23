import sys, re
from attapply import ATTFST
from convertor import *
import glob

alphabet = 'abcdefghijklmnopqrstuvxyz'

def guess(norm, guessed_lemma):
	norm = norm.lower()
	if re.findall('[aeiou]tl$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('[aeiou][^aeiou]+tli$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+yotl$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+huitl$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+tzitzin$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+catl$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+iztli$', norm):
		return(guessed_lemma, 'NOUN', '_', 'Guessed=Yes', [])
	if re.findall('quin[a-z]+tia$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('hual[a-z]+tia$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+huilia$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+quiza$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('[a-z]+ltia$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^xi[a-z]+can$', norm):			# ximellacuahuacan
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^qui[a-z]+([io]|hu)a$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^oquin[a-z]+que$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^tinech', norm):				# tinechitlacoa
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^nimitz', norm):				# nimitzpantia
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^[a-z]+tinemi$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^[a-z]+znequi$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^mo[a-z]+ya$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^mo[a-z]+lia$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^qui[a-z]+ya$', norm):			# quihtohuaya
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^qui[a-z]+tiz$', norm):			# quintlanamictiz
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^[a-z]+zque$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall('^[a-z]+ohua$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall("^mo[a-z]+oa", norm):
		return(guessed_lemma, "VERB", "_", "Guessed=Yes", [])
	if re.findall('tihu[ei]tz(iz|i)?$', norm):
		return(guessed_lemma, 'VERB', '_', 'Guessed=Yes', [])
	if re.findall("tinemi$", norm):
		return(guessed_lemma, "VERB", "_", "Guessed=Yes", [])
	if norm.startswith("xi[^u]"):
		return(guessed_lemma, "VERB", "_", "Guessed=Yes", [])
	if re.findall("tiquiza", norm):
		return (guessed_lemma, 'VERB', "_", "Guessed=Yes", [])
	return (guessed_lemma, 'X', '_', '_', [])

def tag(lexicon, form, norm, idx, analyses):
	lower = norm.lower().strip('*')
	# [{'lemma': 'teotl', 'pos': 'NOUN', 'feats': {'Case': 'Abs'}}] [('teotl<n><abs>', 0.0)]
	#print(analyses, file=sys.stderr)
	
	# TODO: Work out what to do here with multiple analyses
	# 	We should probably do max intersection with the analyses in the lexicon
	guessed_lemma = '_'
	if len(analyses) > 1:
		lemmas = []
		for analysis in analyses:
			lemmas.append(analysis['lemma'])
		lemmas = list(set(lemmas))
		if len(lemmas) == 1:
			guessed_lemma = lemmas[0]

	if len(analyses) == 1:
		addmisc = '_'
		if lower in lexicon:
#			print(idx, norm, '|||', lexicon[lower][0], '|||', analyses[0]['pos'])
			if lexicon[lower][0] != analyses[0]['pos']:
				return (guessed_lemma, lexicon[lower][0], lexicon[lower][1], lexicon[lower][2], [])
			addmisc = lexicon[lower][2]

		analysis = analyses[0]
		#print('@', idx, norm, '|||', analyses[0])
		misc = 'Analysed=Yes'	
		if addmisc != '_':
			misc = addmisc + '|' + misc 
		return (analysis['lemma'], analysis['pos'], '|'.join(['%s=%s' % (i, j) for i, j in analysis['feats'].items()]), misc, analysis['empty'])

	if lower in lexicon:
		return (guessed_lemma, lexicon[lower][0], lexicon[lower][1], lexicon[lower][2], [])

	if norm in lexicon:
		if lexicon[norm][0] == 'PROPN':
			return ('_', lexicon[norm][0], lexicon[norm][1], lexicon[norm][2], [])
	if norm[0] in '0123456789':
		return (norm, 'NUM', '_', '_', [])
	if norm[0].upper() == norm[0] and idx > 1 and norm[0].lower() in alphabet:
		return ('_', 'PROPN', '_', '_', [])
	if norm[0] in '.?!:,;()':
		return (norm, 'PUNCT', '_', '_', [])

	return guess(norm, guessed_lemma)

def read_lexicon(fn, lexicon):
	# FORM			LEMMA			UPOS		UFEATS		MISC
	for lineno, line in enumerate(open(fn).readlines()):
		if line[0] == '#' or line.strip() == '':
			continue
		line = re.sub('\t\t*', '\t', line)
		try:
			token, lemma, upos, ufeats, misc = line.strip().split('\t')
		except:
			print('Error on %d, not enough values to unpack.' % (lineno),file=sys.stderr)
			raise

		if token in lexicon:
			lexicon[token] = (lexicon[token][0] + '|' + upos , '_', '_')
		else:
			if misc == '_':
				lexicon[token] = (upos, ufeats, '_')
			else:
				lexicon[token] = (upos, ufeats, misc)
	return lexicon

def sort_features(ufeats):
	if ufeats != '_' and ufeats != '':
		if '|' in ufeats:
			ufeats = {i.split('=')[0]: i.split('=')[1] for i in ufeats.split('|')}
		else:
			ufeats = {ufeats.split('=')[0]: ufeats.split('=')[1]}
		ufeats = list(ufeats.items())
		ufeats.sort()
		ufeats = '|'.join(['%s=%s' % (i, j) for i, j in ufeats])
	return ufeats

lexicon = read_lexicon('lexicon.tsv', {})
for fn in glob.glob('lexicon/*.lexicon'):
	lexicon = read_lexicon(fn, lexicon)

morfst = ATTFST('../fst/nci.mor.att.gz')
genfst = ATTFST('../fst/nci.gen.att.gz')
convertor = Convertor('tagset.tsv')

total = 0
tagged = 0
analysed = 0

for bloc in sys.stdin.read().split('\n\n'):
	bloc = bloc.strip()

	if not bloc: 
		continue

	comments = [line for line in bloc.split('\n') if line and line[0] == '#']
	lines = [line for line in bloc.split('\n') if line and line[0] != '#']
	new_lines = []
	n_tokens = 0
	n_tagged = 0
	n_analysed = 0

	for line in lines:
		# ID · FORM · LEMMA · UPOS · XPOS · FEATS · HEAD · DEPREL · EDEPS · MISC
		# 0    1      2       3      4      5       6      7        8       9
		row = line.split('\t')

		if '-' in row[0]:
			new_lines.append(row)
			continue
			

		idx = int(row[0])
		form = row[1]
		misc = row[9]
		attrs = {pair.split('=')[0] : pair.split('=')[1] for pair in misc.split('|')}
		norm = attrs['Norm']

		analyses = list(morfst.apply(norm))
		if len(analyses) == 0:
			analyses = list(morfst.apply(norm.lower()))
			
#		print('ANAL', analyses)
		converted_analyses = []
		generated_analyses = {}
		# [{'lemma': 'teotl', 'pos': 'NOUN', 'feats': {'Case': 'Abs'}}] [('teotl<n><abs>', 0.0)]
		for analysis in analyses:
			a = analysis[0]
			c = convertor.convert(a)
			generated_analyses[a] = list(genfst.apply(a))
			converted_analyses.append(c[0])
			#print(form, '|', norm, '|||', c, '|||', a, '|||', generated_analyses, file=sys.stderr)

		if len(converted_analyses) > 0:
			n_analysed += 1
			analysed += 1

		lem, upos, ufeats, addmisc, empties = tag(lexicon, form, norm, idx, converted_analyses)

		row[2] = lem
		row[3] = upos
		row[5] = sort_features(ufeats)

		if addmisc != '_':
			row[9] = row[9] + '|' + addmisc

		if upos != 'X':
			tagged += 1
			n_tagged += 1
		total += 1
		n_tokens += 1

		#print('\t'.join(row))
		new_lines.append(row)
		
		for i, empty in enumerate(empties):
			ufeats = '_'
			if empty['feats'] != set():
				ufeats = '|'.join(list(empty['feats']))
			new_lines.append([row[0] + '.' + str(i+1), '_', empty['lemma'], empty['pos'], '_', ufeats, '_', '_', '_', 'Incorporated=Yes'])

	print('\n'.join(comments))
	if n_tokens > 0:
		print('# tagged = %.2f%%' % (n_tagged/n_tokens*100))
		print('# analysed = %.2f%%' % (n_analysed/n_tokens*100))
	for row in new_lines:
		print('\t'.join(row))
	

	print()

if total != 0:
	print('%d/%d' % (tagged,total), '(%.2f%%); %d/%d (%.2f%%)' % (tagged/total*100, analysed, total, analysed/total*100),file=sys.stderr)
