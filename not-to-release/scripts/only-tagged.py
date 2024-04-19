import sys

exclude = sys.argv[1]

for bloc in sys.stdin.read().split('\n\n'):
	sent_id = ''
	norm = ''
	orig = ''
	valid = True
	for line in bloc.split('\n'):
		if line.count('sent_id') > 0 and exclude in line:
			valid = False
			continue
		if line.count('\t') != 9:
			continue
		row = line.split('\t')
		if '-' in row[0] or '.' in row[0]:
			continue

		if row[3] == 'X' or row[3] == '_':
			valid = False
			continue

	if valid:
		print(bloc)
		print()
