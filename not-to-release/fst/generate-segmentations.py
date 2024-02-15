# Remember to run:
# ln -s ../scripts/attapply.py .
import sys, re
from attapply import ATTFST

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


morfst = ATTFST('nci.mor.att.gz')
genfst = ATTFST('nci.gen.att.gz')


preferences = read_analyses('../scripts/analyses.tsv')

for bloc in sys.stdin.read().split('\n\n'):
	sent_id = ''
	for line in bloc.split('\n'):
		if line.count('sent_id') > 0:
			sent_id = line.split('=')[1].strip()

		row = line.split('\t')
		if len(row) != 10:
			continue
		if '.' in row[0] or '-' in row[0]:
			continue

		orig = row[1]
		norm = re.findall('[^a-zA-Z]Norm=[^| ]+', row[9])[0]
		norm = norm.split('=')[1].strip('*')

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

		generated_forms = {}
		segs = []
		for analysis in analyses:
			a = analysis[0]
			generated_forms[a] = list(genfst.apply(a))
			min_ = sys.maxsize
			best_form = ''
			for generated_form in generated_forms[a]:
				clean_form = re.sub(r'[>·«»~]', '', generated_form[0])
				ld = levenshtein(norm, clean_form)
				if ld[0] < min_:
					min_ = ld[0]
					best_form = re.sub('[»«~]', '', generated_form[0])
			segs.append(re.sub('[>·]', '>', best_form))

		segs = list(set(segs))

		print(generated_forms, file=sys.stderr)
		if len(segs) > 1 or len(segs) == 0: 
			print('@\t%s\t%s\t%s\t%s\t%s' % (sent_id, row[0], orig, norm, norm))
		elif len(segs) == 1 and segs[0].replace('>' ,'').lower() != norm.lower():
			print('!\t%s\t%s\t%s\t%s\t%s' % (sent_id, row[0], orig, norm, norm))
		else:
			print('_\t%s\t%s\t%s\t%s\t%s' % (sent_id, row[0], orig, norm, segs[0]))



