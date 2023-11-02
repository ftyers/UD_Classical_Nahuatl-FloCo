import sys,re

def replace_keep_case(word, replacement, text):
	def func(match):
		g = match.group()
		#print('!',match,'|', g, file=sys.stderr)
		if g.islower(): return replacement.lower()
		if g.istitle(): return replacement.title()
		if g.isupper(): return replacement.upper() 
		return replacement     
	return re.sub(word, func, text, flags=re.I)


line = sys.stdin.readline().strip()
while line:
	
	tokens = re.sub('([:,.!?]+)', ' \g<1> ', line).split(' ')
	normalized_tokens = []
	for token in tokens:
		token = replace_keep_case('muger', 'mujer', token)
		token = re.sub(r'vn([oa])?(s)?$', r'un\g<1>\g<2>', token)		
		token = replace_keep_case('asi', 'así', token)		
		token = replace_keep_case('algun$', 'algún', token)		
		token = replace_keep_case(r'auan$', r'aban', token)
		token = replace_keep_case(r'aua$', r'aba', token)
		token = replace_keep_case('aguero', 'agüero', token)
		token = replace_keep_case('aujan', 'habían', token)
		token = replace_keep_case('auja', 'había', token)	
		token = replace_keep_case('y[uv]a', 'iba', token)
		token = replace_keep_case('quando', 'cuando', token)
		token = re.sub('ç([ao])', 'z\g<1>', token)
		token = re.sub('z([ei])', 'c\g<1>', token)
		token = replace_keep_case('[ji]an$', 'ían', token)
		normalized_tokens.append(token)
	print(re.sub('  *', ' ', ' '.join(normalized_tokens)))

	line = sys.stdin.readline().strip()
