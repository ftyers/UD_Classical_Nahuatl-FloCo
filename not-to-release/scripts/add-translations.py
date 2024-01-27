import sys, re, glob

total = 0
translated = {}

def read_translations(fn, translations):
	global translated
	for line in open(fn):
		line = re.sub('\t\t*', '\t', line)
		if line.strip() == '' or line[0] == '#':
			continue
		sent_id, lang, translation = line.strip().split('\t')
		if sent_id not in translations:
			translations[sent_id] = {}
		if lang not in translated:
			translated[lang] = 0
		translations[sent_id][lang] = translation
	return translations	

translations = {}
for langfile in sys.argv[1:]:
	translations = read_translations(langfile, translations)


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
		for lang in translations[sent_id]:
			new_comments += ['# text[%s] = %s' % (lang, translations[sent_id][lang])]
			translated[lang] += 1
		new_comments += [comments[-1]]
		comments = new_comments
#		translated += 1
	print('\n'.join(comments))
#	if n_tokens > 0:
#		print('# tagged = %.2f%%' % (n_tagged/n_tokens*100))
	for line in lines:
		print(line)

	print()
	total += 1

if total != 0:
	print('Translated:',file=sys.stderr)
	for lang in translated:
		print(' [%s] %d/%d' % (lang, translated[lang],total), '(%.2f%%)' % (translated[lang]/total*100),file=sys.stderr)

