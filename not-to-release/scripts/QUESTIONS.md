* How do we deal with noun incorporation

  * Valency changes, *quinyaochichiuh*

```
29	oqujniauchiuhque	chihua	VERB	_	Aspect=Prior|Number[obj]=Plur|Number[subj]=Plur|Person[obj]=3|Person[subj]=3|Subcat=Tran|Tense=Past|VerbForm=Fin	_	_	_	Folio=13|Paragraph=6|Line=6|Norm=oquinyaochiuhque|Analysed=Yes
29.1	_	yaotl	NOUN	_	_	_	_	_	Incorporated=Yes
```
  
  * Should the `[obj]` here be `[iobj]` ?

* How do we deal with compounding 

  * Of lexical items: *calcuauhuitl*

  * Of relational nouns: 

  * Of both: *ilhuicayollotitech*

* How do we deal with adverbs generated from nouns? *yohualtica*

* How do we deal with classifiers *ontetl*, *centetl*


* How do we deal with ordinals *Inic macuilli capítulo* 

* Should we orthographically normalise based on morphology, e.g. *Imamux* → *Inamox* or *Imamox* ?

* Should we include *h* in words derived from *ihtoa*, e.g. *tlatolli* → *tlahtolli* or *tlatolli*?

* Expressions with *ca* or *catca*

```
Let me recap:
(1) CA (affirmative clause-introducing particle, 'surely, indeed'): w/o saltillo, uninflected;
(2) CAH, CATEH, CATCA (locational verb or copula, 'to be', erroneously "CĀ" by Karttunen): w/ saltillo, verb;
(3) -CA (relational noun, usually in -ti-ca, 'by means of');
(4) -TI-CAH (compouning form of (2), used as aspectual auxiliary: 'to be Ving')
(5) -CĀ- (compounding form of -qui: no-teōpixcā-uh 'my priest')
```

* Because clauses with *ipampa* 

----

## Decisions

### Ordinal numerals and chapters


The word *ic* forms ordinal numerals from cardinal numerals. In Andrews (2001) this is described
as a relational noun that introduces a clause, for example:

```
Ic eyi amoxtli. = With this, the books are three in number; i.e., It is the third book.
```

We treat this slightly differently.

The *Ic* is an `ADJ` which modifies *amoxtli* and takes as a modifier *eyi*. 

```
amod(amoxtli, ic)
nummod(ic, eyi)
obl(motenehua, amoxtli)
```

What else have we considered:

1. The Andrews (2001) analysis:

```
root(eyi)
obl(eyi, ic)
nsubj(eyi, amoxtli)
parataxis(eyi, motenehua)
```

The disadvantage of this is that it makes search difficult, *amoxtli* is hidden deep in the tree as a subject. The 
most important verb in the sentence *motenehua* is then `parataxis` and further down in the tree.


2. An analysis where *ic* is a relational `NOUN` and *eyi* modifies it. Something like *five in-sequence books*
```
obl(motenehua, amoxtli)
nmod(amoxtli, ic)
nummod(ic, eyi)
```

The disadvantage of this is that it reverses the usual direction of relational noun + modifier (e.g. *amoxtli* governs 
*ic* not vice versa.

3. An analysis where *ic* is still a relational `NOUN` but governs both *eyi* and *amoxtli*. Something like *five in-sequence of books*

```
obl(motenehua, ic)
nmod(ic, amoxtli)
nummod(ic, eyi)
```

The downside here is that *amoxtli* appears further down in the tree.
