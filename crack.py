


# script assumes we're using the english alphabet
alphabet = "abcdefghijklmnopqrstuvwxyz"

englishIC = 0.067
# germanIC = 

# relative frequencies of charactes in english text ala http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
relativeFrequenciesEnglish = [12.02, 9.10, 8.12, 7.68, 7.31, 6.95, 6.28, 6.02, 5.92, 4.32, 3.98, 2.88, 2.71, 2.61, 2.30, 2.11, 2.09, 2.03, 1.82, 1.49, 1.11, 0.69, 0.17, 0.11, 0.10, 0.07]

relativeFrequenciesEnglish = [8.167, 1.492, 2.202, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 1.292, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.356, 2.758, 0.978, 2.560, 0.150, 1.994, 0.077]

relativeFrequenciesEnglish = [x/100 for x in relativeFrequenciesEnglish]# decimal not percentage

class Letter:
	letter: ""
	freq: 0
	def __init__(self, letter, freq):
		self.letter = letter
		self.freq = freq

class Match:
	word: ""
	freq: 0
	indexes = []
	def __init__(self, word, freq, indexes):
		self.word = word
		self.freq = freq
		self.indexes = indexes
	

def getPercentDifference(a, b):
	diff = a/b
	diff = abs(diff - 1)
	return diff

def getFrequencies(text):
	countArray = []
	# for each letter in characters, go through text given and count it's frequency
	for char_library in alphabet:
		count = 0
		for char_text in text:
			if char_text == char_library:
				# print(char_text)
				count = count + 1
		countArray.append(count)
	return countArray

def getRelativeFrequencies(frequencies):
	totalCount = 0
	for freq in frequencies:
		totalCount = totalCount + freq
	relativeFrequencies = []
	for freq in frequencies:
		relativeFrequencies.append(freq/totalCount)
	return relativeFrequencies

def printFrequenciesPretty(frequencies):
	print("Frequencies: ")
	for x in range(0, len(frequencies)):
		print(alphabet[x]+": ", end="")
		for x in range(0, frequencies[x]):
			print("*", end="")
		print("")

# go through ciphertext relative frequencies and try to find an equivalent relative frequency in the english relative frequencies
def frequencyAnalysis(relativeFrequencies, cipherText):
	from operator import itemgetter, attrgetter # to sort

	sortObject = []
	for x in range(0, len(alphabet)):
		obj = Letter(alphabet[x], relativeFrequenciesEnglish[x])
		sortObject.append(obj)
	sortedObject = sorted(sortObject, key=lambda obj: obj.freq)
	
	sortObject2 = []
	for y in range(0, len(alphabet)):
		obj2 = Letter(alphabet[y], relativeFrequencies[y])
		sortObject2.append(obj2)
	sortedObject2 = sorted(sortObject2, key=lambda obj: obj.freq)

	print("Alphabet character(freq) - Ciphertext character(freq)")
	for z in range(0, len(alphabet)):
		print(f"{sortedObject[z].letter}({sortedObject[z].freq}) - {sortedObject2[z].letter}({sortedObject2[z].freq})")

def indexOfCoincidence(frequencies):
	totalCount = 0
	for freq in frequencies:
		totalCount = totalCount + freq
	ic = 0
	for x in range(0, len(frequencies)):
		ic = ic + frequencies[x]*(frequencies[x] - 1)
	ic = ic/(totalCount*(totalCount-1))
	return ic

def kasiskiMethod(cipherText):
	matchList = []
	wordLength = 4
	# loop over entire ciphertext
	cursor = 0
	while(cursor <= len(cipherText)):
		indexes = []
		freq = 1
		word = cipherText[cursor:cursor + 4]
		indexes.append(cursor)
		for x in range(cursor + 4, len(cipherText) - 4, 4):
			if cipherText[x:x+4] == word:  # thats a match
				# print(f"match for {word}")
				freq = freq + 1
				# print(freq)
				indexes.append(x)
		if(freq > 1): # if there is a match make an object for it
			# print("oof")
			matchList.append(Match(word, freq, indexes))
		cursor = cursor + wordLength
	print("Kasiski method yields: ")
	print("Matches for word length 4: ")
	for match in matchList:
		print(f"word: {match.word}, occurences: {match.freq}, occurence indexes: {match.indexes}")


def crack(filePath):
	cipherText = open(filePath, 'r').read().lower().replace(" ", "")
	frequencies = getFrequencies(cipherText)
	ic = indexOfCoincidence(frequencies)
	if checkForBasicCiphers(frequencies, ic):
		print(f"IC for {filePath} is awfully close to standard IC of english ({str(ic)}/{str(englishIC)})")
		print("=> this is a basic substitution/transposition (not homophonic)\n")
		print("Trying Kasiski method")
		kasiskiMethod(cipherText)
		# print("Running frequency analysis to find correlations between letters...")
		# relativeFrequencies = getRelativeFrequencies(frequencies)
		# frequencyAnalysis(relativeFrequencies, cipherText)
	else:
		print(f"IC for {filePath} = {ic}")

def checkForBasicCiphers(counts, ic):
	if getPercentDifference(ic, englishIC) < 0.05: #5% similarity seems a stretch for coincidence
		return True
	return False

if __name__ == "__main__":
	import os.path
	from os import path
	while True:
		inputFile = str(input("input filepath to ciphertext: "))
		if path.exists(inputFile):
			print(f"Running analysis on {inputFile}")
			break
		else:
			print(f"File does not exist at filepath {inputFile}")
	crack(inputFile)
	# relativeFrequencies = relativeFrequencies(counts)
	# print(relativeFrequencies)
	# frequencyAnalysis(relativeFrequencies)
