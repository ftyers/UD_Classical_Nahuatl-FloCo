import sys,re

def replace_keep_case(word, replacement, text):
	def func(match):
		g = match.group()
		if g.islower(): return replacement.lower()
		if g.istitle(): return replacement.title()
		if g.isupper(): return replacement.upper() 
		return replacement     
	return re.sub(word, func, text, flags=re.I)


line = sys.stdin.readline()
while line:
	
	tokens = re.sub('([,.!?])', ' \g<1> ', line).split(' ')
	normalized_tokens = []
	for token in tokens:
		token = replace_keep_case('muger', 'mujer', token)
		token = replace_keep_case('vn$', 'un', token)		
		token = replace_keep_case('vna$', 'una', token)		
		token = replace_keep_case('vezes', 'veces', token)		
		token = replace_keep_case('algun$', 'algún', token)		
		token = replace_keep_case('auan$', 'aban', token)
		token = replace_keep_case('aua$', 'aba', token)
		token = replace_keep_case('aguero', 'agüero', token)
		token = replace_keep_case('aujan', 'habían', token)
		token = replace_keep_case('auja', 'había', token)	
		token = replace_keep_case('y[uv]a', 'iba', token)
		token = replace_keep_case('quando', 'cuando', token)
		normalized_tokens.append(token)
	print(' '.join(normalized_tokens))

	line = sys.stdin.readline()
