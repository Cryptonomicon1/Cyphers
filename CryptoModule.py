##Common Variables##
#
# cypher= encrypted message
# key= key to encrypt or decrypt message
# message= plaintext message
# private_key= key to decrypt message
# public_key= key to encrypt message

import enchant
Ench= enchant.Dict("en_US")

from random import randint

# Cyphers & Cracks

def EncryptCeasar(key, message):
	key= int(key) % 26
	cypher= list(message)

	message= UpperToLower(message)

	cypher= TextShift(key, message)

	return ''.join(cypher)

def DecryptCeasar(key, cypher):
	key= -(int(key) % 26)
	message= list(cypher)

	message= TextShift(key, cypher)

	return ''.join(message)

# Use the Enchant Library to Crack Ceasar Cypher
def CrackCeasar(cypher):
	cracked= False
	cyphered_words= ListWords(cypher)
	three_words= list()

	for i in range(3):
		r= randint(0, len(cyphered_words) - 1)
		three_words.append(cyphered_words[r])
		del cyphered_words[r]

	i= 1
	while not cracked and i <= 26:
		cracked= True

		for j in range(3):
			cracked= cracked and Ench.check(DecryptCeasar(i, three_words[j]))
		i= i + 1

	return i - 1

# Utilities

# Take String or List of chars and turn into a list of words
def ListWords(txt):
	temp_string= ''
	temp_list= list()
	txt= list(txt)
	txt.append(' ')

	for i in range(len(txt)):
		if txt[i] != ' ':
			temp_string= temp_string + txt[i]
		else:
			if temp_string != '':
				temp_list.append(temp_string)
			temp_string= ''

	return temp_list

# Shift letters in text by x amount
def TextShift(shift, txt):
	shift= int(shift)
	txt= list(txt)

	for i in range(len(txt)):
		if ord(txt[i]) >= ord('A') and ord(txt[i]) <= ord('Z'):
			txt[i]= chr((((ord(txt[i]) + shift) - ord('A')) % 26) + ord('A'))
		elif ord(txt[i]) >= ord('a') and ord(txt[i]) <= ord('z'):
			txt[i]= chr((((ord(txt[i]) + shift) - ord('a')) % 26) + ord('a'))

	return txt

# Convert Lowercase list of chars to Uppercase list of chars
def LowerToUpper(lower):
	lower= list(lower)
	upper= list(lower)
	alpha_diff= ord('A')-ord('a')

	for i in range(len(lower)):
		if lower[i] >= 'a' and lower[i] <= 'z':
			upper[i]= chr(ord(lower[i]) + alpha_diff)

	return upper

def UpperToLower(upper):
	lower= list(upper)
	upper= list(upper)
	alpha_diff= ord('a')-ord('A')

	for i in range(len(upper)):
		if upper[i] >= 'A' and upper[i] <= 'Z':
			lower[i]= chr(ord(upper[i]) + alpha_diff)

	return lower
