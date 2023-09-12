import sys

left = {}
right = {}

if len(sys.argv) != 3:
	print('merge-trees.py book.conllu trees.conllu')
	sys.exit(-1)

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

	left[sent_id] = bloc

for bloc in open(sys.argv[2]).read().split('\n\n'):
	sent_id = '_'	
	tree = {}
	empty = {}
	if bloc.strip() == '':
		continue
	for line in bloc.split('\n'):
#		print('@@@@', line,file=sys.stderr)
		if line.count('sent_id') > 0:
			sent_id = line.split('=')[1].strip()
			break

	right[sent_id] = bloc 

left_keys = set(list(left.keys()))
right_keys = set(list(right.keys()))

missing = list(left_keys - right_keys)
missing.sort(key=lambda x : int(x.split(':')[1]))

for sent_id in missing:
	print(left[sent_id])
	print()
