#!/usr/bin/env python
import glob
import re

def cleanText(inText):
	# strip out whatever we need here 
	p = re.compile('[,]')
	outText = p.sub('',inText.lower())
	return outText

def processFile(fname):
	print "processing:",fname
	f = open(fname, "r");
	lines=""
	for line in f.readlines():
		lines+=line.strip()+" "
	lines = cleanText(lines)
	# TODO: split by sentence?
	return lines

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