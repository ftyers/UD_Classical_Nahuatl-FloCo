TARGETS = ../not-to-release/conllu/Book_01_-_The_Gods.conllu ../not-to-release/conllu/Book_05_-_The_Omens.conllu 
DEPS = lexicon.tsv normalisation.tsv retokenisation.tsv

all: $(TARGETS)

../not-to-release/conllu/Book_05_-_The_Omens.conllu: ../books/Book_05_-_The_Omens.txt $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../not-to-release/conllu/Book_01_-_The_Gods.conllu: ../books/Book_01_-_The_Gods.txt $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@
