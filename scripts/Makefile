TARGETS = ../not-to-release/conllu/Book_05_-_The_Omens.conllu
DEPS = lexicon.tsv normalisation.tsv retokenisation.tsv

../not-to-release/conllu/Book_05_-_The_Omens.conllu: ../books/Book_05_-_The_Omens.txt $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@
