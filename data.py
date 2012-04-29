#!/usr/bin/env python
###############
# data.py - holds a reference to all the data 
###############

import glob
import re

class data:
	langDirs=[]
	dataDir=""
	test=''
	# Constructor 
	def __init__(self,inputDir,langs):
		self.test='yes'
		self.dataDir=inputDir
		self.langDirs=langs
	
	def preprocess(self):
		print "here",self.langDirs
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
