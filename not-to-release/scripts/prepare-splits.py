import sys, glob, os

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

for line in open('final.tsv'):
	if line.strip() == '':
		continue
	if line[0] == '#':
		continue
	sent, sect, reviewers = line.strip().split('\t')
	if sect == section:
		# Book_05_-_The_Omens.txt:64
		book, sent_no = sent.split(':')
		book = book.split('.')[0]
	
		print(books[book][sent_no],file=of)
		print('',file=of)

of.close()
