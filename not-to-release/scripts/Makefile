TARGETS = ../conllu/Book_01_-_The_Gods.conllu ../conllu/Book_05_-_The_Omens.conllu 
DEPS = lexicon.tsv normalisation.tsv retokenisation.tsv tagset.tsv ../fst/nci.mor.att.gz tag-codex.py

all: $(TARGETS)

../conllu/Book_05_-_The_Omens.conllu: ../books/Book_05_-_The_Omens.txt $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_01_-_The_Gods.conllu: ../books/Book_01_-_The_Gods.txt $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@
