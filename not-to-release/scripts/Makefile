TARGETS = ../conllu/Book_01_-_The_Gods.conllu \
	../conllu/Book_02_-_Ceremonies.conllu \
	../conllu/Book_05_-_The_Omens.conllu \
	../conllu/Book_04_-_The_Art_of_Divination.conllu \
	../conllu/Book_06_-_Rhetoric_and_Moral_Philosophy.conllu \
	../conllu/Book_07_-_The_Sun,_Moon,_Stars,_and_the_Binding_of_the_Years.conllu \
	../conllu/Book_08_-_Kings_and_Lords.conllu \
	../conllu/Book_10_-_The_People.conllu \
	../conllu/Book_11_-_Earthly_Things.conllu \
	../conllu/Book_12_-_The_Conquest_of_Mexico.conllu
DEPS = lexicon.tsv normalisation.tsv retokenisation.tsv tagset.tsv references.tsv subtokens.tsv overrides.tsv analyses.tsv \
	../fst/nci.mor.att.gz tag-codex.py process-codex.py normalisation/* 

all: $(TARGETS)

../conllu/Book_01_-_The_Gods.conllu: ../books/Book_01_-_The_Gods.txt ../trees/Book_01_-_The_Gods.conllu translation/Book_01_-_The_Gods.* $(DEPS)
	python3 process-codex.py $< | python3 add-translations.py translation/Book_01_-_The_Gods.* | python3 tag-codex.py | python3 merge-trees.py ../trees/Book_01_-_The_Gods.conllu > $@

../conllu/Book_02_-_Ceremonies.conllu: ../books/Book_02_-_Ceremonies.tokenised $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_04_-_The_Art_of_Divination.conllu: ../books/Book_04_-_The_Art_of_Divination.txt $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_05_-_The_Omens.conllu: ../books/Book_05_-_The_Omens.txt ../trees/Book_05_-_The_Omens.conllu  translation/Book_05_-_The_Omens.* $(DEPS)
	python3 process-codex.py $< | python3 add-translations.py translation/Book_05_-_The_Omens.* | python3 tag-codex.py | python3 merge-trees.py ../trees/Book_05_-_The_Omens.conllu > $@

../conllu/Book_06_-_Rhetoric_and_Moral_Philosophy.conllu: ../books/Book_06_-_Rhetoric_and_Moral_Philosophy.tokenised $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_07_-_The_Sun,_Moon,_Stars,_and_the_Binding_of_the_Years.conllu: ../books/Book_07_-_The_Sun,_Moon,_Stars,_and_the_Binding_of_the_Years.tokenised $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_08_-_Kings_and_Lords.conllu: ../books/Book_08_-_Kings_and_Lords.txt translation/Book_08_-_Kings_and_Lords.* $(DEPS)
	python3 process-codex.py $< | python3 add-translations.py translation/Book_08_-_Kings_and_Lords.* | python3 tag-codex.py > $@

../conllu/Book_11_-_Earthly_Things.conllu: ../books/Book_11_-_Earthly_Things.tokenised $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_10_-_The_People.conllu: ../books/Book_10_-_The_People.tokenised $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

../conllu/Book_12_-_The_Conquest_of_Mexico.conllu: ../books/Book_12_-_The_Conquest_of_Mexico.tokenised $(DEPS)
	python3 process-codex.py $< | python3 tag-codex.py > $@

