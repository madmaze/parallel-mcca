#MT Final project 4/29/2012 Johns Hopkins University
#Functions that take input sentences and return feature vectors
#vectors can then be used to compare words in the data
#and build a dictionary of words with similar features
#==============================================================
import sys;
import cPickle as pickle

class fVectors:
	lang=''
	# Constructor
	def __init__(self,l):
		self.lang=l
		self.vector={}

	def buildVector(self, sentence):
		# get context vector
		cvect = self.context(sentence)
		# get ortho vector
		ovect = self.ortho(sentence)
		# merge into self.vectors
		for word in ovect:
			if word not in self.vector:
				self.vector[word] = (ovect[word], cvect[word])
			else:
				for mword in cvect[word].keys():
					if mword not in self.vector[word][1]:
						self.vector[word][1][mword] = cvect[word][mword]
					else:
						self.vector[word][1][mword] = self.vector[word][1][mword]+cvect[word][mword]

	#Takes a sentence as input
	#Returns a dictionary with unique words in the sentence as keys
	#and dictionaries for their values
	#where the dictionaries contain the +/- 2 context words as keys
	#and the number of times those words occur as values
	def context(self,sentence):
		s=sentence.split(" ")
		length = len(s)
		wordlist = {}
		cvector = {}
		for n,word in enumerate(s):
			if word in cvector:
				wordlist = cvector[word]
			if n >1:    #check and see there is a word in the -2 position
				temp = s[n-2]

				if len(wordlist)==0:
				    wordlist[temp] = 1
				else:
				    if (temp) in wordlist:
					value = wordlist[temp]
					value = value + 1
					wordlist[temp] = value
				    else:
					wordlist[temp] = 1
			if n >0:    #check and see there is a word in the -1 position
				temp = s[n-1]

				if len(wordlist)==0:
				    wordlist[temp] = 1
				else:
				    if (temp) in wordlist:
					value = wordlist[temp]
					value = value + 1
					wordlist[temp] = value
				    else:
					wordlist[temp] = 1
			if n < (length-1):  #check and see there is a word in the +2 position
				temp = s[n+1]

				if len(wordlist)==0:
				    wordlist[temp] = 1
				else:
				    if (temp) in wordlist:
					value = wordlist[temp]
					value = value + 1
					wordlist[temp] = value
				    else:
					wordlist[temp] = 1
			if n < (length-2): #check and see there is a word in the +1 position
				temp = s[n+2]

				if len(wordlist)==0:
				    wordlist[temp] = 1
				else:
				    if (temp) in wordlist:
					value = wordlist[temp]
					value = value + 1
					wordlist[temp] = value
				    else:
					wordlist[temp] = 1
			cvector[word] = wordlist
			wordlist = {}
		return cvector

	#Takes a sentence as input
	#returns a dictionary with unique words in the sentence as keys
	#and arrays of tri character orthograpic featuers for values
	def ortho(self,sentence):
		s = sentence.split(" ")
		length = len(s)
		ofeatures = []
		ovector = {}
		for n,word in enumerate(s):
		    if word not in ovector:
			taggedword = "#"+word+"#"
			for i in range(0,len(taggedword)):
				trichar = taggedword[i:i+3]
				bichar = taggedword[i:i+2]
				if len(trichar) == 3:
				    ofeatures.append(trichar)
				if len(bichar) == 2:
				    ofeatures.append(bichar)
				ofeatures.append(taggedword[i])
			ovector[word] = ofeatures
			ofeatures=[]
		return ovector


	def saveVectors(self,dirs):
		print "saving ",  dirs + "/" + self.lang + ".p"
		pickle.dump( self.vector, open( dirs + "/" + self.lang + ".p", "wb" ) )

	def loadVectors(self,dirs):
		print "loading ",  dirs + "/" + self.lang + ".p"
		self.vector = pickle.load( open( dirs + "/" + self.lang + ".p", "rb" ) )
