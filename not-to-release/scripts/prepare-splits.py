import sys, glob, os, re

section = sys.argv[1]
output_dir = sys.argv[2]

books = {}

for fn in glob.glob('../conllu/*.conllu'):
	fd = open(fn)
	book = os.path.basename(fn).split('.')[0]	
	if book not in books:
		books[book] = {}
	for bloc in fd.read().split('\n\n'):
		sent_id = ''
		if bloc.strip() == '':
			continue
		for line in bloc.split('\n'):
			if line.count('# sent_id') > 0:
				sent_id = line.split('=')[1].strip().split(':')[1]	
		if sent_id != '':
			books[book][sent_id] = bloc

#for k in books.keys():
#	print(k, books[k].keys())

pattern = 'nci_floco-ud-<SECTION>.conllu'

of = open(output_dir +'/'+pattern.replace('<SECTION>', section), 'w')

totals = {}

for line in open('final.tsv'):
	if line.strip() == '':
		continue
	if line[0] == '#':
		continue
	sent, sect, reviewers, url = re.sub('\t\t*', '\t', line.strip()).split('\t')
	if sect == section:
		# Book_05_-_The_Omens.txt:64
		book, sent_no = sent.split(':')
		book = book.split('.')[0]
		comments = []
		if reviewers != '_' and reviewers != '':
			comments.append('# reviewers = %s' % (reviewers.replace(',',' ')))
		if url != '_' and url != '':
			comments.append('# issue = %s' % (url))

		lines = []
		inSent = False
		for sentline in books[book][sent_no].split('\n'):
			if sentline.strip() == '':
				continue
			if sentline[0] == '#':
				lines.append(sentline)
				continue
			if sentline[0] != '#' and not inSent:
				lines += comments
				lines.append(sentline)
				inSent = True
				continue
			lines.append(sentline)

		outsent = '\n'.join(lines)

		print(outsent,file=of)
		print('',file=of)

of.close()
