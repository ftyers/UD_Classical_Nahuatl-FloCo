import sys, re 

trees = {}
empties = {}

for bloc in open(sys.argv[1]).read().split('\n\n'):
	sent_id = '_'	
	tree = {}
	empty = {}
	if bloc.strip() == '':
		continue
	for line in bloc.split('\n'):
#		print('@@@@', line,file=sys.stderr)
		if line.count('sent_id') > 0:
			sent_id = line.split('=')[1].strip()
		if line[0] == '#':
			continue
		row = line.split('\t')
		if row[0].count('-') > 0:
			continue
		elif row[0].count('.') > 0:
			empty[row[0]] = row
		else:
			tree[row[0]] = row

	trees[sent_id] = tree
	empties[sent_id] = empty

n_trees = 0
n_parsed = 0

for bloc in sys.stdin.read().split('\n\n'):
	sent_id = '_'	
	comments = []
	lines = []
	
	if bloc.strip() == '':
		continue
	for line in bloc.split('\n'):
		if line.count('sent_id') > 0:
			sent_id = line.split('=')[1].strip()
			break


	if sent_id not in trees:
		print(bloc)
		print()	
	else:
		comments = []
		lines = []
		for line in bloc.split('\n'):
			if line[0] == '#':
				comments.append(line)
			else:
				lines.append(line.split('\t'))

		if len(trees[sent_id]) != len([line for line in lines if '.' not in line[0] and '-' not in line[0]]):
			print('ERROR', sent_id, len(trees[sent_id]),'!=',len(lines), file=sys.stderr)
			print('    >', ' '.join(trees[sent_id][row][1] for row in trees[sent_id]), file=sys.stderr)
			print('    <', ' '.join([line[1] for line in lines if '.' not in line[0] and '-' not in line[0]]), file=sys.stderr)
			print(bloc)
		else:
			n_parsed += 1
			for comment in comments:
				print(comment)
			for line in lines:
				idx, form, lem, upos, xpos, feats, head, deprel, edeps, misc = line
	
			
				if idx in trees[sent_id]:
					head = trees[sent_id][idx][6]
					deprel = trees[sent_id][idx][7]
					edeps = trees[sent_id][idx][8]
					line = '\t'.join([idx, form, lem, upos, xpos, feats, head, deprel, edeps, misc])
				print(line)
			print()

	n_trees += 1

print('Trees: %d, Parsed: %d (%.2f%%)' % (n_trees, n_parsed, (n_parsed/n_trees)*100), file=sys.stderr)
