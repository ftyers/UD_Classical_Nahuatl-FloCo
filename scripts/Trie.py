class TrieNode:
	def __init__(self, token=''):
		self.token = token
		self.children = dict()
		self.is_final = False 
		self.replacement = ''

	def display(self,depth=0):
		print(' ' * depth,'|', self.token, self.is_final, self.replacement, len(self.children.keys()))
		for child in self.children:
			self.children[child].display(depth=depth+1)

class PrefixTree:
	def __init__(self):
		self.root = TrieNode()
		
	def insert(self, span, right):
		current = self.root
		for i, token in enumerate(span):
			if token not in current.children:
				prefix = span[0:i+1]
				current.children[token] = TrieNode(prefix)
			current = current.children[token]
		current.is_final = True 
		current.replacement = right 

	def display(self):
		self.root.display()
	
	def find_span(self, span):
		'''
		Returns the TrieNode representing the given span if it exists
		and None otherwise.
		'''
		current = self.root
		for token in span:
#			print('T:',token[0], current.token, current.is_final, current.children.keys())
			if token[0] not in current.children:
#				print('!!!', current.token)
				return None
			current = current.children[token[0]]
	
		if current.is_final:
			return current

	def find(self, span):
		'''
		Returns the TrieNode representing the given span if it exists
		and None otherwise.
		'''
		current = self.root
		for token in span:
			if token not in current.children:
				return None
			current = current.children[token]
	
		if current.is_final:
			return current

	def size(self, current = None):
		'''
		Returns the size of this prefix tree, defined
		as the total number of nodes in the tree.
		'''
		# By default, get the size of the whole trie, starting at the root
		if not current:
			current = self.root
		count = 1
		for word in current.children:
			count += self.size(current.children[word])
		return count
