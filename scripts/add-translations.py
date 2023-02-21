import sys, re

def read_translations(fn):
	translations = {}
	for line in open(fn):
		if line.strip() == '' or line[0] == '#':
			continue
		sent_id, lang, translation = line.strip().split('\t')
		translations[sent_id] = (lang, translation)
	return translations	

translations = read_translations('translations.tsv')

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
		comments = comments[:-1] + ['# text[%s] = %s' % translations[sent_id], comments[-1]]
		translated += 1
	print('\n'.join(comments))
#	if n_tokens > 0:
#		print('# tagged = %.2f%%' % (n_tagged/n_tokens*100))
	for line in lines:
		print(line)

	print()
	total += 1

if total != 0:
	print('%d/%d' % (translated,total), '(%.2f%%)' % (translated/total*100),file=sys.stderr)
