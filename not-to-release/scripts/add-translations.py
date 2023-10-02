import sys, re

def read_translations(fn):
	translations = {}
	for line in open(fn):
		if line.strip() == '' or line[0] == '#':
			continue
		sent_id, lang, translation = line.strip().split('\t')
		if sent_id not in translations:
			translations[sent_id] = []
		translations[sent_id].append((lang, translation))
	return translations	

translations = read_translations(sys.argv[1])

total = 0
translated = 0

for bloc in sys.stdin.read().split('\n\n'):
	bloc = bloc.strip()

	if not bloc: 
		continue

	comments = [line for line in bloc.split('\n') if line and line[0] == '#']
	lines = [line for line in bloc.split('\n') if line and line[0] != '#']

	sent_id = ''
	for comment in comments:
		if comment.startswith('# sent_id'):
			sent_id = comment.split('=')[1].strip()
	if sent_id in translations:
		new_comments = comments[:-1]
		new_comments += ['# text[%s] = %s' % (lang, trad) for lang, trad in translations[sent_id]]
		new_comments += [comments[-1]]
		comments = new_comments
		translated += 1
	print('\n'.join(comments))
#	if n_tokens > 0:
#		print('# tagged = %.2f%%' % (n_tagged/n_tokens*100))
	for line in lines:
		print(line)

	print()
	total += 1

if total != 0:
	print('Translated: %d/%d' % (translated,total), '(%.2f%%)' % (translated/total*100),file=sys.stderr)
