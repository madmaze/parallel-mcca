#MT Final project 4/29/2012 Johns Hopkins University
#Functions that take input sentences and return feature vectors
#vectors can then be used to compare words in the data
#and build a dictionary of words with similar features
#==============================================================
import sys
import math
import cPickle as pickle

class fVectors:
	lang=''
	# Constructor
	def __init__(self,l):
		self.lang=l
		self.vector={}
		self.totalTokens=0
		self.totals={}

	def buildVector(self, sentence):
		# get context vector
		cvect = self.context(sentence)
		# get ortho vector
		# ovect = self.ortho(sentence)
		# merge into self.vectors
		for word in cvect:
			if word not in self.vector:
				self.vector[word] = cvect[word]
			else:
				for mword in cvect[word].keys():
					if mword not in self.vector[word]:
						self.vector[word][mword] = cvect[word][mword]
					else:
						self.vector[word][mword] = self.vector[word][mword]+cvect[word][mword]
	def dumpVec(self):
		#print self.vector
		for k in self.vector:
			print k
			for w in self.vector[k]:
				print "\t",w,self.vector[k][w]
		print "TotalTokens:",self.totalTokens
		for k in self.totals:
			print k, self.totals[k]

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
		r=3
		for n,word in enumerate(s):
			# keep track of words
			if word in self.totals:
				self.totals[word]+=1
			else:
				self.totals[word]=1
			self.totalTokens+=1

			if word in cvector:
				wordlist = cvector[word]

			for i in range(-r,r+1):
				#print n+i, i
				if n+i >= 0 and n+i < length and i != 0:
					tmp=s[n+i]
					if len(wordlist)==0:
					    wordlist[str(i+3)+"_"+tmp] = 1
					else:
					    if tmp in wordlist:
						value = wordlist[str(i+3)+"_"+tmp]
						value = value + 1
						wordlist[str(i+3)+"_"+tmp] = value
					    else:
						wordlist[str(i+3)+"_"+tmp] = 1
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



	def transfromVector(self):
		class breakWord1( Exception ):
			pass

		class breakWord2( Exception ):
			pass

		for word1 in self.vector.keys():
			total = 0
			try:
				for word2 in self.vector[word1].keys():
					try:
						#calculate log liklihood
						k11 = float(self.vector[word1][word2])
						k12 = float(self.totals[word1] - k11)
						k21 = float(self.totals[word2[2:]] - k11)
						k22 = float(self.totalTokens - self.totals[word1] - self.totals[word2[2:]])

						n = float(k11 + k12 + k21 + k22)
						c1 = float(k11 + k12)
						c2 = float(k21 + k22)
						r1 = float(k11 + k21)
						r2 = float(k12 + k22)

						if 0 == k12:
							#print "deleting this one w2.. ",k11,k12,k21,k22, word1,self.totals[word1], word2[2:], self.totals[word2[2:]]," co-occur:",self.vector[word1][word2]
							del self.vector[word1]
							raise breakWord1
						elif 0 == k21:
							#print "deleting this one w2.. ",k11,k12,k21,k22, word1,self.totals[word1], word2[2:], self.totals[word2[2:]]," co-occur:",self.vector[word1][word2]
							del self.vector[word1][word2]
							raise breakWord2

						else:
							try:
								self.vector[word1][word2] = \
									k11 * math.log(float((k11 * n))/(c1 * r1)) \
									+ k12 * math.log(float((k12 * n))/(c1 * r2)) \
									+ k21 * math.log(float((k21 * n))/(c2 * r1)) \
									+ k22 * math.log(float((k22 * n))/(c2 * r2))

								total += self.vector[word1][word2]
							except:
								print "ditching this one.. ",k11,k12,k21,k22, word1, word2[2:]
								print float((k11 * n))/(c1 * r1)
								print float((k12 * n))/(c1 * r2)
								print float((k21 * n))/(c2 * r1)
								print float((k22 * n))/(c2 * r2)
								exit("FAIL!")
								raise breakWord2

					except breakWord2:
						pass
				#normalize
				for word2 in self.vector[word1]:
					self.vector[word1][word2] /= total

			except breakWord1:
				pass

	def cleanupVector(self):
		print "cleaning chomping vector...."

		#remove uncommon words
		for word1 in self.vector.keys():
			if self.totals[word1] < 100:
				del self.vector[word1]

		if self.lang == "fr":
			filename = "french.1.part"
		elif self.lang == "de":
			filename = "german.1.part"
		elif self.lang == "es":
			filename = "spanish.1.part"
		else:
			return


		base = []
		lines = ""
		f = open('./DICT/'+filename, 'r')
		for l in f.readlines():
			bits=l.strip().split("\t")
			if len(bits)==2:
				base.append(bits[1])

		todel=[]
		q=0
		vlen=len(self.vector)
		print "cleaning vector of len:",vlen
		#remove words not in base lexicon
		for word1 in self.vector:
			if q%100==0:
				print (float(q)/vlen)*100,"%"
			for word2 in self.vector[word1]:
				if word2[2:] not in base:
					todel.append((word1,word2))
			q+=1

		for w1,w2 in todel:
			del self.vector[w1][w2]


	def cleanEnglishVector(self,filename):
		print "cleaning english vector...."
		if self.lang != "en":
			print "why are you pruning a non-english vector by a different language?"
			return

		base = []
		lines = ""
		f = open('./DICT/'+filename, 'r')
		for l in f.readlines():
			bits=l.strip().split("\t")
			if len(bits)==2:
				base.append(bits[1])



		todel=[]
		q=0
		vlen=len(self.vector)
		print "vector len:",vlen
		#remove words not in base lexicon
		for word1 in self.vector:
			if q%100==0:
				print (float(q)/vlen)*100,"%"
			for word2 in self.vector[word1]:
				if word2[2:] not in base:
					todel.append((word1,word2))
			q+=1

		for w1,w2 in todel:
			del self.vector[w1][w2]


	def getTestVectors(self,filename,filename2):
		print "get Test Vectors...."

		base = {}
		lines = []
		# read the Dict
		f = open('./DICT/'+filename, 'r')
		for l in f.readlines():
			lines.append(l.strip())

		# only keep what is in the dictionary
		entries = lines
		for e in entries:
			tmp = e.strip().split("\t")
			#print tmp
			if tmp[1] in self.vector:
				base[tmp[1]]=self.vector[tmp[1]] #base[word] = {word->double}
				print "here", base[tmp[1]]
		#so, now base has testword->{foreignword->number} for each testword in dictionary
		#now, we need to translate each foreignword to english (using lang.1.part), to facilitate comparisons
		f.close()
		f = open(filename2, 'r')
		for l in f.readlines():
			lines.append(l.strip())
		tmp = []
		for l in lines:
			tmp.append(l.strip().split()) #tmp = [[english,german]]
		lines = tmp
		entries = {}
		for l in lines:
			entries[l[1]] = l[0] #entries[dictionary-german] = english
		testvect = {}
		for w1 in base: #base = {word->{word->double}}
			final = {}
			for w2 in base[w1]:
				final[w2[:2] + entries[w2[2:]]] = base[w1][w2]
			testvect[w1] = final

		#testvect = foriegn_test_word -> {n_englishword -> number}
		self.vector = testvect
		
	def returnVec(self):
		print len(self.vector)
		print type(self.vector)
		legend=[]
		allVec=[]
		maxLen=0
		for w1 in self.vector:
			#print type(self.vector[w1])
			#print self.vector[w1]
			curLeg=[]
			curVec=[]
			for w2 in self.vector[w1]:
				curLeg.append(w2)
				curVec.append(self.vector[w1][w2])
			if len(curVec)>maxLen:
				maxLen=len(curVec)
			legend.append((w1,curLeg))
			allVec.append(curVec)
			#print "legend:",legend
			#print ""
			#print "allVec:",allVec
			#exit()
		print maxLen
		return self.vector, self.totalTokens
