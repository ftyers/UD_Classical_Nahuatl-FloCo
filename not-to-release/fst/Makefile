all: nci.mor.att.gz nci.gen.att.gz nci.mor.hfstol nci.gen.hfstol nci.orth-norm.hfst

nci.lexc.hfst: nci.lexc
	hfst-lexc --Werror $< -o $@

nci.lexd.att: nci.lexd
	lexd $< > $@

nci.lexd.hfst: nci.lexd.att
	hfst-txt2fst $< -o $@

nci.lexd-pret.hfst: nci.lexd.hfst preterite.xfst.hfst
	hfst-compose -1 nci.lexd.hfst -2 preterite.xfst.hfst -o $@

nci.lexc.gen.hfst: nci.lexc.hfst nci.twol.hfst
	hfst-compose-intersect -1 nci.lexc.hfst -2 nci.twol.hfst | hfst-eliminate-flags -o $@

nci.lexc.mor.hfst: nci.lexc.gen.hfst nci.mor.twol.hfst
	hfst-compose-intersect -1 nci.lexc.gen.hfst  -2 nci.mor.twol.hfst | hfst-invert -o $@

nci.gen.hfst: nci.lexd-pret.hfst nci.twol.hfst
	hfst-compose-intersect -1 nci.lexd-pret.hfst -2 nci.twol.hfst -o $@

nci.mor.hfst: nci.gen.hfst nci.mor.twol.hfst
	hfst-compose-intersect -1 nci.gen.hfst  -2 nci.mor.twol.hfst | hfst-invert -o $@

nci.orth-norm.hfst: orth-norm.lexc
	hfst-lexc $< -o $@

%.xfst.hfst: %.xfst
	hfst-regexp2fst -S $< -o $@

%.twol.hfst: %.twol
	hfst-twolc $< -o $@

%.att.gz: %.att
	gzip -f -9 $<

%.att: %.hfst
	hfst-fst2txt $< -o $@

%.hfstol: %.hfst
	hfst-fst2fst -w $< -o $@

cov: nci.mor.hfstol coverage.sh
	./coverage.sh $<
