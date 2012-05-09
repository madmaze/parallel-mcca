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
	res={}
	# Constructor
	def __init__(self,inputDir,langs,processed):
		self.test='yes'
		self.dataDir=inputDir
		self.langDirs=langs
		self.procDir=processed
		self.enVecs = fVectors.fVectors("en")
		self.esVecs = fVectors.fVectors("es")

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
				for t in self.esVecs.vector.keys():
					if t != '':
						pairings[t]=self.compareVecs((s,self.enVecs.vector[s]), (t,self.esVecs.vector[t]))

				self.res[s]=pairings
				q+=1

	def compareVecs(self, S, T):
		vS,vT = self.joinVecs(S,T)

		return 1

	def joinVecs(self, vecA, vecB):
		#print vecA
		# unpack vector
		legend=[]
		combA=[]
		combB=[]
		s, (vAo,vAc) = vecA
		print s, vAo, vAc
		t, (vBo,vBc) = vecB
		print t,vBo,vBc

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

		for i in range(0,len(legend)):
			print legend[i],combA[i],combB[i]

		#print vecB

		exit()
		return combA, combB

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
