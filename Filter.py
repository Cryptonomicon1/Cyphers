# This is just a script that helped me filter
# Raw_Dictionary.txt which is a text file full
# of 100,000ish english words from most common
# to least commonly used.

from random import randint

def FilterDictionary():
	lines = []
	directory = "Raw_Dictionary.txt"

	#count number of lines in Raw_Dictionary.txt
	with open(directory) as txt:
		line_count = len(txt.readlines())

	txt.close()
	txt = open(directory)

	#Read Raw_Dictionary line by line into a list
	for i in range(line_count):
		lines.append(txt.readline())

	#Delete Extra  Whitespaces
	for i in range(line_count):
		line = lines[i]
		temp_line = ''
		for char in line:
			if char != ' ':
				temp_line = temp_line + char.lower()
		lines[i] = temp_line

	#Delete Comment Lines
	i = 0
	while i != len(lines):
		if lines[i][0] == '#':
			del lines[i]
		i = i + 1

	#Delete Repeat Words
	#This takes FOREVER!
	#Too bad idk multithreading.
	i = 0
	while i != len(lines):
		j = i
		while j != len(lines):
			if (i != j) and (lines[i] == lines[j]):
				del lines[j]
			else:
				j = j + 1
		if ((i + 1) % 1000) == 0 or i == 0:
			print("Checking Redundancies @ Line", i + 1, "/", len(lines))
		i = i + 1

	#Write Batch of words to single file
	directory = "Dictionary.txt"

	txt.close()
	txt = open(directory, 'w')

	text = ''.join(lines)
	txt.write(text)

	txt.close()

	#Find Longest Word Length
	longest_word_length = 0

	for line in lines:
		if longest_word_length < len(line) - 1:
			longest_word_length = len(line) - 1

	#Make files for each word length
	#Note: I tried like hell to not write
	#files with no words. However, nothing
	#worked :(. I noticed that the
	#largest word was a website url at
	#a length of 65 chars. The next
	#largest word was a length of 22
	#chars. So, I just started at 22.

	word_length = longest_word_length
	word_length = 22

	while word_length != 0:
		directory = 'Words_Len_' + str(word_length) + '.txt'
		txt = open(directory, 'w')
		words = []
		i = 0

		while(i != len(lines)):
			if word_length == len(lines[i]) - 1:
				words.append(lines[i])
				del lines[i]
				i = i - 1
			i = i + 1


		word_length = word_length - 1
		words = ''.join(words)
		txt.write(words)
		txt.close()
