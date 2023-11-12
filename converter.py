import sys,re

def replace_keep_case(word, replacement, text):
	def func(match): #defines the function
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
		
		token = replace_keep_case('jendo$','iendo', token)
		token = replace_keep_case('sauandija','sabandija', token)
		token = replace_keep_case('onze','once', token)
		token = replace_keep_case('muger', 'mujer', token)
		token = replace_keep_case('mesmo', 'mismo', token)
		token = replace_keep_case(r'a[uv]an$', r'aban', token)
		token = replace_keep_case(r'a[uv]a$', r'aba', token)
		token = replace_keep_case('aujan', 'habían', token)
		token = replace_keep_case('auja', 'había', token)	
		token = replace_keep_case('y[uv]a', 'iba', token)
		token = replace_keep_case('quando', 'cuándo', token)
		token = replace_keep_case('nueua', 'nueva', token)
		token = replace_keep_case('dexa', 'deja', token)
		token = replace_keep_case('mjedo', 'miedo', token)
		token = replace_keep_case('camjno', 'camino', token)
		token = replace_keep_case('vezes', 'veces', token)
		token = replace_keep_case('penetratiuo', 'penetrativo', token) # i dont think this is right
		token = replace_keep_case('aue', 'ave', token)		

		#removing stuff
		token = replace_keep_case('pass', 'pas', token)
		token = replace_keep_case('habla me', 'hablame', token)
	
		#for accents
		token = replace_keep_case('asi', 'así', token)
		token = replace_keep_case('oya', 'oía', token)
		token = replace_keep_case('alli', 'allí', token)
		token = replace_keep_case('mas$', 'más', token)
		token = replace_keep_case('aguero', 'agüero', token)
		token = replace_keep_case('algun$', 'algún', token)		
		token = replace_keep_case('parecera', 'parecerá', token)		

		# for splitting words
		token = replace_keep_case('ala', 'a la', token)
		token = replace_keep_case('della', 'de ella', token)
		token = replace_keep_case('dest[oa]', 'de est\g<1>', token)
		token = replace_keep_case('poruentura', 'por ventura', token)

		
		# re.sub functions 
		token = re.sub('ç([ao])', 'z\g<1>', token)
		token = re.sub(r'vn([oa])?(s)?$', r'un\g<1>\g<2>', token)			
		token = re.sub('z([ei])', 'c\g<1>', token)
		token = re.sub('aua([n])?','aba\g<1>', token)
		token = re.sub('d([ie])z', 'd\g<1>c', token)	
		token = re.sub('[ji]a([n])?$', 'ía\g<1>', token)
		token = replace_keep_case('quj', 'qui', token) # this is for next time i work on the file,
		# going to change this for qujera/qujere/qujen stuff^
		
		# cual shenanigans?
		if (token == 'qualquiera'):
			token = replace_keep_case('qualqiera', 'cualquiera', token)

		elif (token == 'qualqujera'):
			token = replace_keep_case('qualqujera', 'cualquiera', token)

		else:		
			token = replace_keep_case('qual', 'cuál', token)		
	
		normalized_tokens.append(token)

	print(re.sub('  *', ' ', ' '.join(normalized_tokens)))

	line = sys.stdin.readline().strip()
