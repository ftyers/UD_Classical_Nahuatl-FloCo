all:
	hfst-lexc nci.lexc -o nci.lexc.hfst
	hfst-twolc nci.twol -o nci.twol.hfst
	hfst-compose-intersect -1 nci.lexc.hfst -2 nci.twol.hfst -o nci.gen.hfst
	hfst-invert nci.gen.hfst -o nci.mor.hfst
	hfst-fst2txt nci.mor.hfst -o nci.mor.att
