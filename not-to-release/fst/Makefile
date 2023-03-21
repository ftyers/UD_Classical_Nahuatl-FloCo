all:
	# <s_pl1>quiza<v><iv><past>:ti>quiz>que
	hfst-lexc --Werror nci.lexc -o nci.lexc.hfst
	hfst-twolc nci.twol -o nci.twol.hfst
	hfst-twolc nci.mor.twol -o nci.mor.twol.hfst
	# <aug><s_sg3><on>«tlalli<n>»miqui<v><iv><impf>:o>on>tlal·miqui>ya
	hfst-compose-intersect -1 nci.lexc.hfst -2 nci.twol.hfst | hfst-eliminate-flags -o nci.gen.hfst
	hfst-compose-intersect -1 nci.gen.hfst  -2 nci.mor.twol.hfst | hfst-eliminate-flags | hfst-invert -o nci.mor.hfst
	hfst-fst2fst -w nci.mor.hfst -o nci.mor.hfstol
	hfst-fst2fst -w nci.gen.hfst -o nci.gen.hfstol
	hfst-fst2txt nci.mor.hfst -o nci.mor.att
	hfst-fst2txt nci.gen.hfst -o nci.gen.att
	gzip -f -9 nci.mor.att 
	gzip -f -9 nci.gen.att 
