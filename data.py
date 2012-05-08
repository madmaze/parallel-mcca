#!/usr/bin/env python
###############
# data.py - holds a reference to all the data 
###############

import glob
import re
import fVectors

class data:
	langDirs=[]
	dataDir=""
	procDir=""
	vecSubdir="vecs"
	test=''
	enVecs = fVectors.fVectors("en")
	esVecs = fVectors.fVectors("es")
	res={}
	# Constructor 
	def __init__(self,inputDir,langs,processed):
		self.test='yes'
		self.dataDir=inputDir
		self.langDirs=langs
		self.procDir=processed
	
	def runMCCA(self):
		print "in MCCA..."
		q=0
		# iterate over all source words
		for s in self.enVecs.vector.keys():
			if q<10 and s != '':
				print s, len(self.enVecs.vector[s][0]),len(self.enVecs.vector[s][1])
				print self.enVecs.vector[s][0]
				print self.enVecs.vector[s][1]
				print " "
				pairings={}
				# iterate over all target words
				for t in self.esVecs.vector.keys():
					pairings[t]=(self.compareOrtho(s, t),self.compareContext(s, t))
					
				self.res[s]=pairings
				q+=1
				
	def compareOrtho(self, S, T):
		return 1
		
	def compareContext(self, S, T):
		return 1
	
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
		
		#print lines
		# split by .
		lines = self.cleanText(lines).split(". ")
		tmp=[]
		
		# split by ?
		for l in lines:
			tmp += l.split("? ")
	
		lines=tmp[:]
		tmp=[]
		
		# split by !
		for l in lines:
			tmp += l.split("! ")
		
		lines=tmp[:]
		tmp=[]	
		
		# split by !
		for l in lines:
			tmp += l.split('" ')
		
		lines=tmp[:]
		tmp=[]
		
		for l in lines:
			tmp += l.split(' "')
		
		lines=tmp[:]
		tmp=[]
		p2 = re.compile('[?.,"\']')
		for l in lines:
			if l != '':
				t = p2.sub(' ',l).strip()
				tmp.append(t)
				#print t
		return tmp[:]
