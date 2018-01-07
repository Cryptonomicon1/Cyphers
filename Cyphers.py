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
# fac = factor
# lil = little
# low = lower
# prep = prepare
# punc = punctuation
# up = upper

from random import randint
from math import ceil
from string import ascii_lowercase
import enchant
# Note: Below I imported the nltk library.
# 		In this library, I imported the
# 		words corpus. Some computers may
# 		not have the words corpus
#		downloaded. So, you may have to
#		run nltk.download().

# PWL = enchant.request_pwl_dict("Dictionary.txt")
EnDict = enchant.Dict("en_US")
# PWLDict = enchant.DictWithPWL("en_US", "Dictionary.txt", "Raw_Dictionary.txt")

class Cyphers():

	def __init__(self):
		self.low_alph = list(ascii_lowercase)
		self.shift_alph = [[]]
		self.alph_index = {}
		self.words = self.InitWordList()
		self.words_len = len(self.words)
		self.com_wds = self.InitComWords()
		self.crack_deny_ratio = 0.45 # Raise ratio to deny more false positives in cracking

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
		key = 0
		crack = False

		while key < 26 and not crack:
			message = self.DecryptCeasar(key, cypher)
			words = []
			crack = self.RealWords(message)
			key = key + 1

		return key - 1

	def EncryptVigenere(self, key, message):
		cypher = ''

		key = self.NoPunc(key)
		message = self.NoPunc(message)
		key = self.RepeatKey(key, len(message))

		for i in range(len(message)):
			shift = (self.alph_index[ key[i] ] + 1) % 26
			cypher = cypher + self.ShiftText(shift, message[i])

		return cypher

	def DecryptVigenere(self, key, cypher, warn=False):
		message = ''

		key = self.NoPunc(key)
		cypher = self.NoPunc(cypher)
		key = self.RepeatKey(key, len(cypher), warn)

		for i in range(len(cypher)):
			shift = (self.alph_index[ key[i] ] +1) % 26
			message = message + self.ShiftText(-shift, cypher[i])

		return message

	def CrackVigenere(self, cypher):
		crack = False
		attempt = 0
		wd_lens = self.SortIndL2S( self.CountFactors( self.SubSpace(cypher) ) )

		for i in range(len(wd_lens)): wd_lens[i] += 1

		wd_ind = 0
		len_ind = 0
		print("Cracking...")
		print("Trying", wd_lens[len_ind], "letter words.")

		# While present attempt didn't work keep crackin'
		while not crack:
			if attempt % 100 == 0:
				print("Attempt", attempt, "/", len(self.words[ wd_lens[len_ind]-1 ])-1)

			attempt += 1

			if wd_ind < len(self.words[ wd_lens[len_ind]-1 ])-1:
				wd_ind += 1

			elif len_ind < 3:
				len_ind += 1
				wd_ind = 0
				attempt = 0
				print(" ")
				print("There are no more", wd_lens[len_ind]-1, "letter words.")
				print("The next best estimate is", wd_lens[len_ind], "letter words.")

			else:
				print("Crack Failure")
				return None

			if self.RealWords( self.DecryptVigenere( self.words[ wd_lens[len_ind]-1 ][wd_ind], cypher)):
				good_input = False
				while not good_input:
					key_wd = self.words[ wd_lens[len_ind]-1 ][wd_ind]
					print(" ")
					print("Possible Key:", self.words[ wd_lens[len_ind]-1 ][wd_ind])
					if len(cypher) > 50:
						mess = self.DecryptVigenere(key_wd, cypher[:50])
						print("Possibility:", ' '.join(self.TokWords(mess)), "...")
					else:
						mess = self.DecryptVigenere(key_wd, cypher)
						print("Possibility:", ' '.join(self.TokWords(mess)))
					print(" ")
					cont = input("Continue Cracking? y or n: ")

					if cont == 'y':
						good_input = True
					elif cont == 'n':
						good_input = True
						crack = True
					else:
						print("Bad Input, try again.")

		return self.words[ wd_lens[len_ind]-1 ][wd_ind]

	##Utility Functions##

	# Shift each character in a string or list by a number of letters
	def ShiftText(self, shift, text):
		shift = shift % 26
		shifted_text = ''

		for char in text:
			index = self.alph_index[char]
			shifted_text = shifted_text + self.shift_alph[shift][index]

		return shifted_text

	def RepeatKey(self, key, message_length, warn=True):
		if len(key) < message_length:
			if warn:
				print(" ")
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
		end = len(txt) - 1
		word_len = len(txt)
		words = []
		txt_map = list(range(len(txt)))
		words_map = []

		while len(txt) > 0 and word_len > 0:
			if EnDict.check(txt[beg:end]) and word_len == txt_map[end-1] - txt_map[beg] + 1:
				i  = 0
				while i < len(words_map) and words_map[i] < txt_map[beg]:
					i += 1

				words_map = words_map[:i] + [txt_map[beg]] + words_map[i:]
				words = words[:i] + [txt[beg:end]] + words[i:]
				txt = txt[:beg] + txt[end:]
				txt_map = txt_map[:beg] + txt_map[end:]
				beg = 0
				end = len(txt)
				word_len = len(txt)

			elif end < len(txt):
				beg += 1
				end += 1

			elif word_len > 1:
				beg = 0
				word_len -= 1
				end = word_len

			else:
				words.append(txt[:2])
				txt = txt[2:]
				beg = 0
				end = len(txt)
				word_len = len(txt)

		return words

	# Imports 100 Most Common Words
	def InitComWords(self):
		with open("Hundred.txt", 'r') as f:
			words = f.read().splitlines()

		return words

	# Initializes Words
	def	InitWordList(self):
		import nltk
		from nltk.corpus import words

		w = words.words()

		for i in range(len(w)):
			w[i] = w[i].lower()

		wd = []
		for i in range(20): wd.append([])

		for i in range(len(w)):
			for j in range(1, 20):
				if len(w[i]) == j:
					wd[j-1].append(w[i])

		return wd

	# Finds if there are enough real words
	def RealWords(self, txt):
		letters = 0

		for com_wd in self.com_wds:
			com_wd_len = len(com_wd)
			for i in range(len(txt)-com_wd_len):
				if txt[i:i+com_wd_len] == com_wd:
					letters += com_wd_len

		if len(txt)*self.crack_deny_ratio <= letters:
			return True
		else:
			return False

	# Return a list of counts of the spaces between
	# substrings.
	def SubSpace(self, cypher):
		low_chk = 3 # Smallest repeating string to check (inclusive)
		high_chk = 5 # Largest repeating string to check (non-inclusive)
		space_count = []

		for word_len in range(low_chk, high_chk): #---------------------------------Different Word Lengths
			for chker in range(len(cypher)-word_len): #-----------------------------String that checks
				for chkee in range(chker+1, len(cypher)-word_len): #------------------String that is checked
					if cypher[chker:chker+word_len] == cypher[chkee:chkee+word_len]:
						space_count.append(abs(chker - chkee))
						break

		return space_count

	# Returns counts of a range
	# of factors from list of numbers.
	def CountFactors(self, nums):
		low_fac = 2 # Lowest Factor to Start with (inclusive)
		high_fac = 21 # Highest Factor to end on (non-inclusive)

		factor_counts = [0]*(high_fac-1)

		for num_ind in range(len(nums)):
			for facs in range(low_fac, high_fac):
				if nums[num_ind] % facs == 0:
					factor_counts[facs-1] += 1

		return factor_counts

	# Returns sorted list of indexes
	# from largest to smallest
	def SortIndL2S(self, nums):
		ind_ord = list(range(len(nums)))
		flip_flag = True

		while flip_flag:
			flip_flag = False
			for i in range(1, len(nums)):
				if nums[i-1] < nums[i]:
					temp = nums[i-1]
					nums[i-1] = nums[i]
					nums[i] = temp
					temp = ind_ord[i-1]
					ind_ord[i-1] = ind_ord[i]
					ind_ord[i] = temp
					flip_flag = True

		return ind_ord
