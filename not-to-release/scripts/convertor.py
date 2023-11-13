import sys , re

class Convertor(object):
	"""
	A class to convert from Apertium-style analyses to UD-compatible analyses by
	means of a sequence of priority-ordered rules.

	Parameters
	----------
	rule_file: str
		A path to the location of the TSV file containing the tagset
		conversion rules.
		Each rule is composed of 9 columns:
			1. Priority
			2. Input lemma
			3. Input POS
			4. Input features
			5. Input dependency relation (unused)
			6. Output lemma
			7. Output POS
			8. Output features
			9. Output dependency relation (unused)

	"""
	def __init__(self, rule_file):
		self.conversion_rules = self._load_conversion_rules(rule_file)
		self.input_patterns = re.compile('(' + '|'.join(self.conversion_rules['sym']) + ')')

	def _convert_tags(self, tags):
		"""
		Convert from the tag format in the TSV rule-file to tags that will match
		the Apertium analyses, e.g. v|tv → <v><tv> and p1|sg → <p1><sg>

		Parameters
		----------
		tags: str
			A sequence of tags separated by the pipe symbol, |

		Returns
		----------
		str
			A sequences of tags encased in less-than and greater-than < >
		"""

		if tags != '':
			return '<' + tags.replace('|', '><') + '>'
		return tags

	def _load_conversion_rules(self, fn):
		"""
		Loads the conversion rules and scores each rule. Longer rules are
		scored higher, rules containing lemmas are scored higher.

		Parameters
		----------
		fn: str
			A path to the location of the TSV file containing the
			tagset conversion rules.

		Returns
		----------
		dict
			A dictionary containing a set of symbols used for matching and a list of
			substitution rules.
		"""

		rules = {'sym': set(), 'sub': []}
		for line in open(fn):
			if line[0] == '#' or line.strip() == '':
				continue
			row = line.strip().split('\t')
			priority = int(row[0])
			score = priority
			inn = [re.sub('^_$', '', i) for i in row[1:5]]
			out = [re.sub('^_$', '', i) for i in row[5:]]

			if inn[0] != '':
				score += 4
			if inn[1] != '':
				score += 3
			if inn[2] != '':
				score += (2 * len(inn[2].split('|')))
			if inn[3] != '':
				score += 1

			inn = [inn[0],
					self._convert_tags(inn[1]), self._convert_tags(inn[2]), inn[3]]
			rules['sym'].add(inn[1])
			rules['sym'].add(inn[2])
			rules['sub'].append((score, inn, out))

		rules['sym'] = list(rules['sym'])
		rules['sym'].sort(key=lambda x: len(x), reverse=True)
		rules['sub'].sort(reverse=True)
		return rules

	def _apply_rules(self, msd, analysis):

		# FIXME: This is broken, we need to make sure that there are full matches before
		# setting the POS, examples: itechpa, tlein, coatl
		for (priority, inn, out) in self.conversion_rules['sub']:
			pos_pat = set([inn[1]])
			remainder = msd - pos_pat
			intersect = msd.intersection(pos_pat)
			if intersect == pos_pat:
				analysis['pos'] = out[1]
				if out[2] != '' and msd - set(inn[2]) != msd:
					for i in out[2].split('|'):
						analysis['feats'].add(i)
				msd = remainder
			feats_pat = set([inn[2]])
			remainder = msd - feats_pat
			intersect = msd.intersection(feats_pat)
			if intersect == feats_pat:
				for i in out[2].split('|'):
					analysis['feats'].add(i)
				msd = remainder

		return msd, analysis


	def _convert(self, a, s):
		"""
		Convert an analysis to UD using the conversion rules, rules
		are applied in priority order.

		Parameters
		----------
		a: str
			An Apertium-compatible analysis, e.g. <s_sg1>quiza<v><iv><pret>, note
			that by this point there should be no subwords.

		Returns
		----------
		dict
			A dictionary containing a lemma, a part-of-speech and a
			set of Feature=Value pairs.
		"""
		analysis = {'lemma': '', 'pos': '', 'feats': set(), 'empty':[]}
		incorporated = re.findall('«[^»]+»', a)
		incorporated_surface = re.findall('«[^»]+»', s)
		a = re.sub('«[^»]+»', '', a)
		tags = [i for i in self.input_patterns.findall(a) if not i == '']
		msd = set(tags)
		analysis['lemma'] = re.sub('<[^>]+>', '', a)
	
		msd, analysis = self._apply_rules(msd, analysis)

		# Convert set of Feature=Value pairs to dictionary of Feature:Value
		analysis['feats'] = {i.split('=')[0]: i.split('=')[1]
					for i in analysis['feats'] if not i == ''}

		if len(incorporated) != len(incorporated_surface):
			print('CONVERTOR: WARNING:', incorporated, incorporated_surface, file=sys.stderr)
			for incorp in incorporated:
				empty = {'surface': '_', 'lemma': '', 'pos': '', 'feats': set()}
				tags = [i for i in self.input_patterns.findall(incorp) if not i == '']
				msd = set(tags)
				
				empty['lemma'] = re.sub('<[^>]+>', '', incorp[1:-1])
				msd, empty = self._apply_rules(msd, empty)
				analysis['empty'].append(empty)	
		else:
			for incorp, incorp_surf in zip(incorporated, incorporated_surface):
				empty = {'surface':re.sub('[»«]', '', incorp_surf),'lemma': '', 'pos': '', 'feats': set()}
				tags = [i for i in self.input_patterns.findall(incorp) if not i == '']
				msd = set(tags)
				empty['lemma'] = re.sub('<[^>]+>', '', incorp[1:-1])
				msd, empty = self._apply_rules(msd, empty)
				analysis['empty'].append(empty)	


		return analysis

	def convert(self, analysis_, surface_=''):
		"""
		The main function for conversion, takes a full analysis, including possible
		subwords, e.g. ya<adv>+<s_sg1>quiza<v><iv><pret> and returns a list of
		syntactic words.

		Parameters
		----------
		analysis_: str
			An Apertium-compatible analysis.

		Returns
		----------
		list
			A list of the component analyses by syntactic word.
		"""

		analysis = []
		subwords = analysis_.split('+')
		if surface_ != '':
		#	print('CONVERT:', analysis_, '|', surface_, file=sys.stderr)
			if surface_.count('·') == len(subwords):
				subsurface = surface_.split('·')
				for word, surface in zip(subwords, subsurface):
					analysis.append(self._convert(word, surface))
			else:
				for word in subwords:
					analysis.append(self._convert(word, surface_))
		else:
			for word in subwords:
				analysis.append(self._convert(word, surface_))

		return analysis
