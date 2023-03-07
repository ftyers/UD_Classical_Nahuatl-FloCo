TARGETS = ../not-to-release/conllu/Book_05_-_The_Omens.conllu

../not-to-release/conllu/Book_05_-_The_Omens.conllu: ../books/Book_05_-_The_Omens.txt
	python3 process-codex.py $< | python3 tag-codex.py > $@
