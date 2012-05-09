#!/usr/bin/env python
###############
# data.py - holds a reference to all the data
###############

import glob
import re
import fVectors
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

class data:
	langDirs=[]
	dataDir=""
	procDir=""
	vecSubdir="vecs"
	test=''
	enVecs = fVectors.fVectors("en")
	esVecs = fVectors.fVectors("es")
	# Constructor
	def __init__(self,inputDir,langs,processed):
		self.test='yes'
		self.dataDir=inputDir
		self.langDirs=langs
		self.procDir=processed

	def runMCCA(self):
		print "in MCCA..."

	def saveVecs(self):
		self.enVecs.saveVectors(self.procDir+"/"+self.vecSubdir)

	def loadVecs(self):
		self.enVecs.loadVectors(self.procDir+"/"+self.vecSubdir)

	def genVectors(self):
		print "in genVectors().."
		for l in self.langDirs:
			print l
			for f in glob.glob(self.procDir + "/"+ l + "/*"):
				# chop out non input files.. aka readme
				if f.find(".processed") > 0:
					inFile = open(f, "r");
					for line in inFile.readlines():
						if l == "en":
							self.enVecs.buildVector(line.strip())
						elif l == "es":
							self.esVecs.buildVector(line.strip())


	def preprocess(self):
		print "in preprocessing().."
		for l in self.langDirs:
			cnt=0
			for f in glob.glob(self.dataDir + "/" + l + "/*"):
				# chop out non input files.. aka readme
				if f.find(".txt") > 0:
					cnt+=1
					self.saveProcessed(self.processFile(f),"PROCESSED/"+l+"/"+str(cnt))

			print l, cnt, "input files"

	def cleanText(self,inText):
		# strip out whatever we need here
		p = re.compile('[,]')
		outText = p.sub('',inText)
		return outText

	def saveProcessed(self,data,fname):
		fout = open(fname+".processed", "w")
		for line in data:
			#print line
			fout.write(line+"\n")


	def processFile(self,fname):
		print "processing:",fname
		f = open(fname, "r");
		lines=""
		for line in f.readlines():
			lines+=line.strip()+" "

		lines = self.cleanText(lines)
		tmp=[]

		wordpunct_tokenize(lines)
		tmp+=[word_tokenize(t) for t in sent_tokenize(lines)]
		lines=tmp[:]
		tmp=[]
		print lines

#		p2 = re.compile('[?.,"\'\[\]:;]')
		for l in lines:
			for m in ["?",".",",","\"","\'\'","``","\'","[","]",":",";",":","!"]:
				x = l.count(m)
				for i in range(x):
					l.remove(m)
		tmp = lines
		# return lines
		return tmp[:]
