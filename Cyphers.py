##Common Variables##
#
# cypher= encrypted message
# key= key to encrypt or decrypt message
# message= plaintext message
# private_key= key to decrypt message
# public_key= key to encrypt message
#
##Common Abbreviations##
#
# alph = alphabet
# char = character
# cryption = encryption, decryption, and/or cypher crack method
# cryptonomicon = list of cryption functions (reference to Lovecraft's Necronomicon)
# low = lower
# prep = prepare
# punc = punctuation
# up = upper

from random import randint
from math import ceil
from string import ascii_lowercase
import enchant

# PWL = enchant.request_pwl_dict("Dictionary.txt")
EnDict = enchant.Dict("en_US")
# PWLDict = enchant.DictWithPWL("en_US", "Dictionary.txt", "Raw_Dictionary.txt")

class Cyphers():

	def __init__(self):
		self.low_alph = list(ascii_lowercase)
		self.shift_alph = [[]]
		self.alph_index = {}

		# Create Dictionary of alphabet indexes 'a' = 0, 'b'= 1, 'c' = 2, etc.
		for char in self.low_alph:
			self.alph_index.update({char : ord(char) - ord('a')})

		# Create Table of shifted Alphabets self.shift_alph[0] = ['a', 'b', 'c'...],
		# self.shift_alph[1] = ['b', 'c', 'd'...], self.shift_alph[2] = ['c', 'd', 'e'...], etc
		for row in range(26):
			shift = row
			for col in range(26):
				letter = ascii_lowercase[(col + shift) % 26] # make letter with shift = row
				self.shift_alph[row].append(letter) # add letter to column
			self.shift_alph.append([]) # add new row

	##Main Functions##

	def EncryptCeasar(self, key, message):
		message = self.NoPunc(message)
		return self.ShiftText(key, message)

	def DecryptCeasar(self, key, cypher):
		cypher = self.NoPunc(cypher)
		return self.ShiftText(-key, cypher)

	def CrackCeasar(self, cypher):
		return 0

	def EncryptVigenere(self, key, message):
		cypher = ''

		key = self.NoPunc(key)
		message = self.NoPunc(message)
		key = self.RepeatKey(key, len(message))

		for i in range(len(message)):
			shift = (self.alph_index[ key[i] ] + 1) % 26
			cypher = cypher + self.ShiftText(shift, message[i])

		return cypher

	def DecryptVigenere(self, key, cypher):
		message = ''

		key = self.NoPunc(key)
		cypher = self.NoPunc(cypher)
		key = self.RepeatKey(key, len(cypher))

		for i in range(len(cypher)):
			shift = (self.alph_index[ key[i] ] +1) % 26
			message = message + self.ShiftText(-shift, cypher[i])

		return message

	def CrackVigenere(self, cypher):
		return 0

	##Utility Functions##

	# Shift each character in a string or list by a number of letters
	def ShiftText(self, shift, text):
		shift = shift % 26
		shifted_text = ''

		for char in text:
			index = self.alph_index[char]
			shifted_text = shifted_text + self.shift_alph[shift][index]

		return shifted_text

	def RepeatKey(self, key, message_length):
		if len(key) < message_length:
			print("Warning: key length is less than message length")
			print("This issue will make the encryption weak.")
			print(" ")

			repeat_key = ceil( message_length / len(key) )
			original_key = key

			for i in range(1, repeat_key):
				key = key + original_key

		return key

	# Delete all punctuation, spaces, and lowercase the letters
	def NoPunc(self, text_in):
		text_out = ''

		for char in text_in:
			if char.lower() in self.low_alph:
				text_out = text_out + char.lower()

		return text_out

	# Tokanizes string of words without spaces
	def TokWords(self, txt):
		beg = 0
		end = len(txt)
		words = []

		while beg < len(txt):
			while end > beg:
				if EnDict.check(txt[beg:end]):

					if beg > 0:
						words.append(txt[:beg])
						beg = 0

					words.append(txt[beg:end])
					txt = txt[end:]
					end = len(txt)
				else:
					end = end - 1

			beg = beg + 1
			end = len(txt)

		return words

