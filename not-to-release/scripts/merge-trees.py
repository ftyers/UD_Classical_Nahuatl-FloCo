import sys, re 

def get_token_lines(bloc):
	rows = bloc.split('\n')
	lines = []	
	for line in rows:
		if line[0] == '#':
			continue
		row = line.split('\t')
		if row[0].count('-') > 0 or row[0].count('.') > 0:
			continue
		else:
			lines.append(row)

	return lines
	
n_trees = 0
n_parsed = 0

trees = {}
empties = {}

stats = {}

n_tokens = 0
n_tokens_head = 0
n_tokens_head_deprel = 0
	

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
			stats[sent_id] = [0, 0, 0]
		if line[0] == '#':
			continue
		row = line.split('\t')
		if row[0].count('-') > 0:
			continue
		elif row[0].count('.') > 0:
			empty[row[0]] = row
		else:
			tree[row[0]] = row
			stats[sent_id][0] += 1
			# id,form,lem,upos,xpos,feat,head,deprel,edep,misc
			if row[6] != '_':
				n_tokens_head += 1
				stats[sent_id][1] += 1
			if row[7] != '_':
				n_tokens_head_deprel += 1
				stats[sent_id][2] += 1

	trees[sent_id] = tree
	empties[sent_id] = empty

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

	n_tokens += len(get_token_lines(bloc))

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
			print('# heads = %.2f%%' % ((stats[sent_id][1]/stats[sent_id][0])*100))
			print('# relations = %.2f%%' % ((stats[sent_id][2]/stats[sent_id][0])*100))
			for line in lines:
				idx, form, lem, upos, xpos, feats, head, deprel, edeps, misc = line
			
				if idx in trees[sent_id]:
					if upos == 'X' or '|' in upos:
						if trees[sent_id][idx][3] != upos:
							upos = trees[sent_id][idx][3]
					head = trees[sent_id][idx][6]
					deprel = trees[sent_id][idx][7]
					edeps = trees[sent_id][idx][8]

				line = '\t'.join([idx, form, lem, upos, xpos, feats, head, deprel, edeps, misc])
				print(line)
			print()

	n_trees += 1

info = (n_trees, n_parsed, (n_parsed/n_trees)*100, n_tokens, n_tokens_head, (n_tokens_head/n_tokens)*100, n_tokens_head_deprel, (n_tokens_head_deprel/n_tokens)*100)
print('Trees: %d, Parsed: %d (%.2f%%) | Tokens: %d, Heads: %d (%.2f%%), Deprels: %d (%.2f%%)' % info, file=sys.stderr)
