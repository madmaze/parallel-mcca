#!/usr/bin/env python
import glob
import re

def cleanText(inText):
	# strip out whatever we need here 
	p = re.compile('[,]')
	outText = p.sub('',inText)
	return outText

def processFile(fname):
	print "processing:",fname
	f = open(fname, "r");
	lines=""
	for line in f.readlines():
		lines+=line.strip()+" "
	
	print lines
	# split by .
	lines = cleanText(lines).split(". ")
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

def main(dataDir, langDirs):
	for l in langDirs:
		cnt=0
		for f in glob.glob(dataDir + "/" + l + "/*"):
			# chop out non input files.. aka readme
			if f.find(".txt") > 0:
				cnt+=1
				print processFile(f)
				exit()

		print l, cnt, "input files"

if __name__ == "__main__":
	langs=["en","es"]
	inputDir="./DATA"
	main(inputDir,langs)