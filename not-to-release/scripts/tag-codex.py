import sys, re
from attapply import ATTFST
from convertor import *
import glob

alphabet = 'abcdefghijklmnopqrstuvxyz'

def levenshtein(u, v):
	prev = None
	curr = [0] + list(range(1, len(v) + 1))

	# Operations: (SUB, DEL, INS)
	prev_ops = None
	curr_ops = [(0, 0, i) for i in range(len(v) + 1)]
	for x in range(1, len(u) + 1):
		prev, curr = curr, [x] + ([None] * len(v))
		prev_ops, curr_ops = curr_ops, [(0, x, 0)] + ([None] * len(v))
		for y in range(1, len(v) + 1):
			delcost = prev[y] + 1
			addcost = curr[y - 1] + 1
			subcost = prev[y - 1] + int(u[x - 1] != v[y - 1])
			curr[y] = min(subcost, delcost, addcost)
			if curr[y] == subcost:
				(n_s, n_d, n_i) = prev_ops[y - 1]
				curr_ops[y] = (n_s + int(u[x - 1] != v[y - 1]), n_d, n_i)
			elif curr[y] == delcost:
				(n_s, n_d, n_i) = prev_ops[y]
				curr_ops[y] = (n_s, n_d + 1, n_i)
			else:
				(n_s, n_d, n_i) = curr_ops[y - 1]
				curr_ops[y] = (n_s, n_d, n_i + 1)
	return curr[len(v)], curr_ops[len(v)]


def guess(norm, guessed_lemma, guessed_upos, misc):
	norm = norm.lower()
	guessed_misc = '_'
	if misc.strip('_') != '':
		guessed_misc = misc + '|Guessed=Yes'
	else:
		guessed_misc = 'Guessed=Yes'
	if re.findall('[aeiou]tl$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[aeiou][^aeiou]+tli$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('(in|in|no|mo)[a-z]+huan$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+yotl$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+huitl$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('(i|in|im)[a-z]+ayo$', norm):				# imanahuayo
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+tzitzin$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+(tilmatli|icpalli)$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+catl$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+iztli$', norm):
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('[a-z]+tin$', norm):					# zoquitecontotontin
		return(guessed_lemma, 'NOUN', '_', guessed_misc, [])
	if re.findall('o[a-z]+aya$', norm):					# ontlapalohuaya
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('tla[a-z]+aya$', norm):					# tlatlauhtiaya
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('quin[a-z]+tia$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('hual[a-z]+tia$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('[a-z]+nenca$', norm):					#onentlamattinenca
		return(guessed_lemma, 'VERB', '_', guessed_misc, []) 
	if re.findall('o[a-z]+manca$', norm):					#otlamahuizmamanca
		return(guessed_lemma, 'VERB', '_', guessed_misc, []) 
	if re.findall('o[a-z]+i[tc]o$', norm):					#otechtoquilico
		return(guessed_lemma, 'VERB', '_', guessed_misc, []) 
	if re.findall('[a-z]+huilia$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('[a-z]+quiza$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('[a-z]+ltia$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^xi[a-z]+can$', norm):			# ximellacuahuacan
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^qui[a-z]+([io]|hu)a$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^oquin[a-z]+que$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^tinech', norm):				# tinechitlacoa
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^nimitz', norm):				# nimitzpantia
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^[a-z]+tinemi$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^[a-z]+znequi$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^mo[a-z]+ya$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^mo[a-z]+lia$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^qui[a-z]+ya$', norm):			# quihtohuaya
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^qui[a-z]+tiz$', norm):			# quintlanamictiz
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^[a-z]+zque$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall('^[a-z]+ohua$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall("^mo[a-z]+oa", norm):
		return(guessed_lemma, "VERB", "_", guessed_misc, [])
	if re.findall('tihu[ei]tz(iz|i)?$', norm):
		return(guessed_lemma, 'VERB', '_', guessed_misc, [])
	if re.findall("tinemi$", norm):
		return(guessed_lemma, "VERB", "_", guessed_misc, [])
	if norm.startswith("xi[^u]"):
		return(guessed_lemma, "VERB", "_", guessed_misc, [])
	if re.findall("tiquiza", norm):
		return (guessed_lemma, 'VERB', "_", guessed_misc, [])
	if guessed_upos != '_':
		return (guessed_lemma, guessed_upos, '_', misc, [])
	return (guessed_lemma, 'X', '_', misc, [])

def tag(lexicon, form, norm, idx, analyses):
	lower = norm.lower().strip('*')
	# [{'lemma': 'teotl', 'pos': 'NOUN', 'feats': {'Case': 'Abs'}}] [('teotl<n><abs>', 0.0)]
	#print('@', form,'|||', analyses, file=sys.stderr)
	
	# TODO: Work out what to do here with multiple analyses
	# 	We should probably do max intersection with the analyses in the lexicon
	guessed_lemma = '_'
	guessed_upos = '_'
	misc = '_'
	if lower in lexicon:
		guessed_lemma = lexicon[lower][0]

	if len(analyses) > 1:
		misc = 'Ambiguous=Yes|Analysed=Yes'	
		lemmas = []
		uposes = []
		
		for analysis in analyses:
			lemmas.append(analysis['lemma'])
			uposes.append(analysis['pos'])
		lemmas = list(set(lemmas))
		uposes = list(set(uposes))
		if len(lemmas) == 1:
			guessed_lemma = lemmas[0]
		if len(uposes) == 1:
			guessed_upos = uposes[0]

	if len(analyses) == 1:
		addmisc = '_'
		if lower in lexicon:
			#print(idx, norm, '|||', lexicon[lower][1], '|||', analyses[0]['pos'], '|||', lexicon[lower], file=sys.stderr)
			if lexicon[lower][1] != analyses[0]['pos']:
				return (guessed_lemma, lexicon[lower][1], lexicon[lower][2], lexicon[lower][3], [])
			addmisc = lexicon[lower][3]

		analysis = analyses[0]
		#print('@', idx, norm, '|||', analyses[0])
		misc = 'Analysed=Yes'	
		if addmisc != '_':
			misc = addmisc + '|' + misc 
		return (analysis['lemma'], analysis['pos'], '|'.join(['%s=%s' % (i, j) for i, j in analysis['feats'].items()]), misc, analysis['empty'])

	if lower in lexicon:
		#print('>>', idx, norm, '|||', lexicon[lower][1], '|||', lexicon[lower], file=sys.stderr)
		return (guessed_lemma, lexicon[lower][1], lexicon[lower][2], lexicon[lower][3], [])

	if norm in lexicon:
		if lexicon[norm][1] == 'PROPN':
			guessed_lemma = lexicon[norm][0]
			return (guessed_lemma, lexicon[norm][1], lexicon[norm][2], lexicon[norm][3], [])
	if norm[0] in '0123456789':
		return (norm, 'NUM', '_', '_', [])
	if norm[0].upper() == norm[0] and idx > 1 and norm[0].lower() in alphabet:
		return (guessed_lemma, 'PROPN', '_', '_', [])
	if norm[0] in '.?!:,;()':
		return (norm, 'PUNCT', '_', '_', [])

	return guess(norm, guessed_lemma, guessed_upos, misc)

def read_lexicon(fn, lexicon):
	# FORM			LEMMA			UPOS		UFEATS		MISC
	for lineno, line in enumerate(open(fn).readlines()):
		if line[0] == '#' or line.strip() == '':
			continue
		line = re.sub('\t\t*', '\t', line)
		try:
			token, lemma, upos, ufeats, misc, url = line.strip().split('\t')
		except:
			print('! Error on %d, not enough values to unpack.' % (lineno),file=sys.stderr)
			print('!', line, line.split('\t'), file=sys.stderr)
			raise

		if token in lexicon and upos not in lexicon[token][1].split('|'):
			lexicon[token] = (lexicon[token][0], lexicon[token][1] + '|' + upos , '_', '_')
			if lemma not in lexicon[token][0].split('|'):
				lexicon[token] = (lexicon[token][0] + '|' + lemma, lexicon[token][1], '_', '_')
		else:
			if misc == '_':
				lexicon[token] = (lemma, upos, ufeats, '_')
			else:
				lexicon[token] = (lemma, upos, ufeats, misc)
	return lexicon

def read_analyses(fn):
	preferences = {}
	for lineno, line in enumerate(open(fn).readlines()):
		if line[0] == '#' or line.strip() == '':
			continue
		line = re.sub('\t\t*', '\t', line)
		try:
			form, analysis = line.strip().split('\t')
		except:
			print('! Error on %d, not enough values to unpack.' % (lineno),file=sys.stderr)
			print('!', line, line.split('\t'), file=sys.stderr)
			raise
		preferences[form] = [(analysis, 0.0)]
	return preferences	

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

preferences = read_analyses('analyses.tsv')

sents = 0
total = 0
tagged = 0
analysed = 0
lemmatised = 0
clean = 0

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
	n_lemmatised = 0

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

		if '*' not in norm:
			clean += 1 

		analyses = list(morfst.apply(norm))
		if len(analyses) == 0:
			analyses = list(morfst.apply(norm.lower()))

		trimmed_analyses = []
		# prefer lexicalised
		for analysis in analyses:
			if '+' in analysis[0]:
				continue
			if '<caus>' in analysis[0] or '<appl>' in analysis[0]:
				continue
			trimmed_analyses.append(analysis)
	
		if len(trimmed_analyses) > 0:
			analyses = trimmed_analyses

		if norm in preferences:
			analyses = preferences[norm]
		elif norm.lower() in preferences:
			analyses = preferences[norm.lower()]
			
#		print('ANAL', analyses)
		converted_analyses = []
		generated_forms = {}
		# [{'lemma': 'teotl', 'pos': 'NOUN', 'feats': {'Case': 'Abs'}}] [('teotl<n><abs>', 0.0)]
		for analysis in analyses:
			a = analysis[0]
			generated_forms[a] = list(genfst.apply(a))
			min_ = sys.maxsize
			best_form = ''
			for generated_form in generated_forms[a]:
				clean_form = re.sub(r'[>·«»~]', '', generated_form[0])
				if '«' in generated_form[0] or '·' in generated_form[0]:
					ld = levenshtein(form, clean_form)
					if ld[0] < min_:
						min_ = ld[0]
						best_form = generated_form[0]
#					print('FORM:', form, clean_form,'|', ld,'|', min_, '|', best_form, file=sys.stderr)
					
			c = convertor.convert(a, best_form)
			if c[0] not in converted_analyses:
				converted_analyses.append(c[0])
#			print(form, '|', norm, '|||', c, '|||', a, '|||', generated_analyses, file=sys.stderr)

		if len(converted_analyses) > 0:
			n_analysed += 1
			analysed += 1

		lem, upos, ufeats, addmisc, empties = tag(lexicon, form, norm, idx, converted_analyses)

		row[2] = lem
		row[3] = upos
		row[5] = sort_features(ufeats)

		if addmisc != '_':
			row[9] = row[9] + '|' + addmisc

		if upos != 'X' or (upos == 'X' and 'Analysed=Yes' in addmisc):
			tagged += 1
			n_tagged += 1

		if lem != '_':
			lemmatised += 1
			n_lemmatised += 1
		total += 1
		n_tokens += 1

		#print('\t'.join(row))
		new_lines.append(row)
		
		for i, empty in enumerate(empties):
			ufeats = '_'
			if empty['feats'] != set():
				ufeats = '|'.join(list(empty['feats']))
			new_lines.append([row[0] + '.' + str(i+1), empty['surface'], empty['lemma'], empty['pos'], '_', ufeats, '_', '_', '_', 'Incorporated=Yes'])

	print('\n'.join(comments))
	if n_tokens > 0:
		print('# tagged = %.2f%%' % (n_tagged/n_tokens*100))
		print('# lemmatised = %.2f%%' % (n_lemmatised/n_tokens*100))
		print('# analysed = %.2f%%' % (n_analysed/n_tokens*100))
	for row in new_lines:
		print('\t'.join(row))
	

	print()

if total != 0:
	print('Normalised: %d/%d (%.2f%%)' % (clean, total, clean/total*100), file=sys.stderr, end=' | ')
	print('Tagged: %d/%d (%.2f%%)' % (tagged, total, tagged/total*100), file=sys.stderr, end=' | ')
	print('Lemmatised: %d/%d (%.2f%%)' % (lemmatised, total, lemmatised/total*100), file=sys.stderr, end=' | ')
	print('Analysed: %d/%d (%.2f%%)' %  (analysed, total, analysed/total*100), file=sys.stderr)
