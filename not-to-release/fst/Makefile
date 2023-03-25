all: nci.mor.att.gz nci.gen.att.gz

nci.lexc.hfst: nci.lexc
	hfst-lexc --Werror $< -o $@

nci.lexd.att: nci.lexd
	lexd $< > $@

nci.lexd.hfst: nci.lexd.att
	hfst-txt2fst $< -o $@

nci.lexd-pret.hfst: nci.lexd.hfst preterite.xfst.hfst
	hfst-compose -1 nci.lexd.hfst -2 preterite.xfst.hfst -o $@

nci.gen.hfst: nci.lexc.hfst nci.twol.hfst
	hfst-compose-intersect -1 nci.lexc.hfst -2 nci.twol.hfst | hfst-eliminate-flags -o $@

nci.mor.hfst: nci.gen.hfst nci.mor.twol.hfst
	hfst-compose-intersect -1 nci.gen.hfst  -2 nci.mor.twol.hfst | hfst-invert -o $@

nci.lexd.gen.hfst: nci.lexd-pret.hfst nci.twol.hfst
	hfst-compose-intersect -1 nci.lexd-pret.hfst -2 nci.twol.hfst -o $@

nci.lexd.mor.hfst: nci.lexd.gen.hfst nci.mor.twol.hfst
	hfst-compose-intersect -1 nci.lexd.gen.hfst  -2 nci.mor.twol.hfst | hfst-invert -o $@

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
