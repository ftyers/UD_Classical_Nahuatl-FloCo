# Files

* `nci.lexc`: Lexicon and morphotactics
* `nci.twol`: Phonological rules


# Stuff you can do:

Print all strings:

```bash
$ hfst-fst2strings nci.mor.hfst
amoxpol:amoxtli<n><aug>
amoxton:amoxtli<n><dim>
amoxtzitzin:amoxtli<n><rev><pl>
amoxtzin:amoxtli<n><rev>
amoxtli:amoxtli<n><abs>
amox:amoxtli<n>
```

Analyse a token:

```bash
$ echo "noyollo" | hfst-lookup nci.mor.hfst 
noyollo	<px1sg>yollotl<n>	0,000000
```
