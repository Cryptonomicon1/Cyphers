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

class Cryptonomicon():

	def __init__(self):
		self.low_alph = list(ascii_lowercase)
		self.shift_alph = [[]]
		self.alph_index = {}
		self.biggest_word_length = 22
		self.word_list_percent = 100

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
		crack = False
		for key in range(26):
			m = self.DecryptCeasar(key, cypher)
			words_match = 0
			for word_size in range(self.biggest_word_length, 2, -1):
				words = self.ListWordsOfLength(10, word_size)
				for word in words:
					for word_beg in range(len(m) - word_size):
						word_end = word_beg + word_size
						if m[word_beg:word_end] == word:
							words_match = words_match + 1
						if words_match == 3:
							crack = True
						if crack:
							break
					if crack:
						break
				if crack:
					break
			if crack:
				break

		return key

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

	def AddWord(self, top_percent, word):
		word = self.NoPunc(word)
		word_length = len(word)
		directory = self.WordFileDir(word_length)
		line_count = self.LineCount(directory)
		file = open(directory, 'r')

		insert_loc = round(line_count * top_percent / 100)

		words = []
		for i in range(line_count):
			if insert_loc == i:
				words.append(word + '\n')
			words.append(file.readline())

		words = ''.join(words)

		file = open(directory, 'w')
		file.write(words)
		file.close()

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
			if char.isalpha():
				text_out = text_out + char.lower()

		return text_out

	# Returns file directory of word file given word length
	def WordFileDir(self, word_size):
		return 'Words_Len_' + str(word_size) + '.txt'

	# Opens file and returns number of lines in the file
	def LineCount(self, directory):
		with open(directory) as file:
			line_count = len(file.readlines())
		return line_count

	# List words with the inputted length
	def ListWordsOfLength(self, word_list_percent, word_length):
		directory = self.WordFileDir(word_length)

		line_count = self.LineCount(directory)
		line_count = round(word_list_percent * line_count / 100)

		file = open(directory, 'r')
		words = []
		for i in range(line_count):
			words.append(file.readline()[:-1])

		return words

	# Separates strings of words without spaces
	# the best a computer can do.
	def TokanizeWords(self, text):
		text_memory = text

		for word_size in range(self.biggest_word_length, 0, -1):
			words = self.ListWordsOfLength(self.word_list_percent, word_size)
			for word in words:
				word_beg = 0
				while word_beg <= (len(text) - word_size):
					word_end = word_beg + word_size
					if word == text_memory[word_beg:word_end]:
						text = text[:word_end] + ' ' + text[word_end:]
						text_memory = text_memory[:word_beg] + self.Spaces(word_size + 1) + text_memory[word_end:]
						word_beg = word_beg + 1
					word_beg = word_beg + 1

		return text

	def Spaces(self, num):
		spaces = ''
		for i in range(num):
			spaces = spaces + ' '
		return spaces
