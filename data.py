#!/usr/bin/env python
###############
# data.py - holds a reference to all the data
###############

import glob
import re
import fVectors
import math
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer

class data:
	langDirs=[]
	dataDir=""
	procDir=""
	vecSubdir="vecs"
	test=''
	res={}
	# Constructor
	def __init__(self,inputDir,langs,processed):
		self.test='yes'
		self.dataDir=inputDir
		self.langDirs=langs
		self.procDir=processed
		self.enVecs = fVectors.fVectors("en")
		self.esVecs = fVectors.fVectors("de")

	def runMCCA(self):
		print "in MCCA..."
		q=0
		# iterate over all source words
		for s in self.enVecs.vector.keys():
			if q<10 and s != '':
				#print s, len(self.enVecs.vector[s][0]),len(self.enVecs.vector[s][1])
				#print self.enVecs.vector[s][0]
				#print self.enVecs.vector[s][1]
				#print " "
				pairings={}
				# iterate over all target words
				localMax=0
				bestMatch=[]
				for t in self.esVecs.vector.keys():
					if t != '':
						#pairings[t]=self.compareVecs((s,self.enVecs.vector[s]), (t,self.esVecs.vector[t]))
						r=self.compareVecs((s,self.enVecs.vector[s]), (t,self.esVecs.vector[t]))
						if r > localMax:
							localMax=r
							#bestMatch=((s,self.enVecs.vector[s]), (t,self.esVecs.vector[t]))
							bestMatch=(s, t)
				if q%100==0:
					print q, localMax, bestMatch
				self.res[s]=(localMax, bestMatch)
				q+=1
		for x in sorted(self.res.iteritems(), key=operator.itemgetter(1)):
			print x, self.res[x]

	def compareVecs(self, S, T):
		vS,vT,legend = self.joinVecs(S,T)
		r = self.cosSimilarity(vS,vT)
		return r

	def cosSimilarity(self, vecA, vecB):
		dotProd=0
		vAsum=0
		vBsum=0
		for i in range(0,len(vecA)):
			dotProd+=vecA[i]*vecB[i]
			vAsum+=vecA[i]*vecA[i]
			vBsum+=vecB[i]*vecB[i]
		return (dotProd/(math.sqrt(vAsum)*math.sqrt(vBsum)))

	def joinVecs(self, vecA, vecB):
		#print vecA
		# unpack vector
		legend=[]
		combA=[]
		combB=[]
		s, (vAo,vAc) = vecA
		#print s, vAo, vAc
		t, (vBo,vBc) = vecB
		#print t,vBo,vBc

		# Build orthographic vector
		for Ao in vAo:
			legend.append(Ao)
			combA.append(1)
			if Ao in vBo:
				combB.append(1)
			else:
				combB.append(0)

		for Bo in vBo:
			if Bo not in legend:
				legend.append(Bo)
				combB.append(1)
				combA.append(0)
		# build context vector?

		#for i in range(0,len(legend)):
		#	if combA[i]==combB[i]:
		#		print legend[i],combA[i],combB[i],"<here"
		#
		#print vecB
		#exit()
		return combA, combB, legend

	def saveVecs(self):
		self.enVecs.saveVectors(self.procDir+"/"+self.vecSubdir)
		self.esVecs.saveVectors(self.procDir+"/"+self.vecSubdir)

	def loadVecs(self):
		self.enVecs.loadVectors(self.procDir+"/"+self.vecSubdir)
		self.esVecs.loadVectors(self.procDir+"/"+self.vecSubdir)

	def genVectors(self):
		print "in genVectors().."
		for l in self.langDirs:
			print l
			for f in glob.glob(self.procDir + "/"+ l + "/*"):
				# chop out non input files.. aka readme
				if f.find(".processed") > 0:
					print f
					inFile = open(f, "r");
					for line in inFile.readlines():
						if l == "en":
							#print line.strip()
							self.enVecs.buildVector(line.strip())
							#print "en"
						elif l == "es":
							#print "es"
							#print line.strip()
							self.esVecs.buildVector(line.strip())


	def preprocess(self):
		print "in preprocessing().."
		for l in self.langDirs:
			cnt=0
			for f in glob.glob(self.dataDir + "/" + l + "/*"):
				# chop out non input files.. aka readme
				if f.find(".txt") > 0:
					cnt+=1
					self.saveProcessed(self.processFile(f,l),"PROCESSED/"+l+"/"+str(cnt))

			print l, cnt, "input files"

	def cleanText(self,inText):
		# strip out whatever we need here
		p = re.compile('[,]')
		outText = p.sub('',inText)
		out=""
		print "Sanitizing input data..."
		for w in outText.split(" "):
			try:
				t=unicode(w,'UTF-8')
				out += " "+w
			except:
				print w, " not included"
			#containsUnknown=0
			#for l in w:
			#	if ord(l) > 128:
			#		containsUnknown=1
			#if containsUnknown == 0:
			#	out += " "+w
		return out

	def saveProcessed(self,data,fname):
		fout = open(fname+".processed", "w")
		for line in data:
			#print type(line)
			fout.write(" ".join(line.encode('UTF-8'))+"\n")


	def processFile(self,fname,lang):
		print "processing:",fname
		f = open(fname, "r")
		lines=""
		for line in f.readlines():
			#print line.strip()
			try:
				trash=unicode(line.strip(),'UTF-8')
				lines+=line.strip()+" "
			except:
				for w in line.strip().split(" "):
					try:
						trash = unicode(w,'UTF-8')
						lines += w + " "
					except:
						print w, " not included"

		#lines = unicode(self.cleanText(lines),'UTF-8')
		lines = unicode(lines,'UTF-8')
		tmp=[]

		wordpunct_tokenize(lines)
		tmp+=[word_tokenize(t) for t in sent_tokenize(lines)]
		lines=tmp[:]
		tmp=[]

		print "removing punctuation and function words... "
		#TODO: add other function words -> if/then/else, etc
		if lang == "en":
			bad = ["he","she","it","I","you"
					,"they","we"
					,"him","her","me"
					,"them","us"
					,"his","her","my","your"
					,"their","our"
					,"hers","mine","yours"
					,"thers","ours"
					,"a","an","the"]
		elif lang == "es":
			bad = ["el","ella","usted","yo","tu"
					,"ellos","ellas","ustedes","nosotros","vosotros"
					,"le","la","te","me"
					,"les","las","nos","vos"
					,"un","una","el","la"
					,"unos","unas","los","las"]
		elif lang == "de":
			bad = [] #TODO: put german pronouns and articles here
		elif lang == "fr":
			bad = [] #TODO: put french pronouns and articles here
		else:
			bad = []

		for l in lines:
			for m in ["?",".",",","\"","\'\'","``","\'","[","]",":",";",":","!"]:
				l = removeAll(l,m)
			for n in bad:
				l = removeAll(l,n)

		tmp = lines
		lines = tmp[:]
		tmp = []

		print "stemming... "
		if lang == "en":
			stemmer = SnowballStemmer("english")
		elif lang == "es":
			stemmer = SnowballStemmer("spanish")
		elif lang == "de":
			stemmer = SnowballStemmer("german")
		elif lang == "fr":
			stemmer = SnowballStemmer("french")
		else:
			fail = "you screwed up your languages... find the right stemmer yourself!! cur lang: " + lang
			exit(fail)

		for s in lines:
			for w in s:
				#print w
				tmp.append(stemmer.stem(w))

		return tmp[:]

def removeAll(l,token):
	x = l.count(token)
	for i in range(x):
		l.remove(token)
	return l
