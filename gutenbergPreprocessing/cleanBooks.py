#!/usr/bin/env python
import glob
import random
import os
#from nltk.stem import SnowballStemmer
books=[]
lang='es'
dirname='./'+lang+'_txt/'
for fname in glob.glob(dirname+"*"):
        # chop out non input files.. aka readme
        if fname.find(".txt") > 0 and fname.find("README") == -1:
                books.append(fname)
books2={}
for b in books:
	path=b.split("/")
	fname=path[len(path)-1]
	fname=fname.split(".")[0]
	enc=""
	if '-' in fname:
		bits=fname.split("-")
		#print bits
		fname=bits[0]
		enc=bits[1]
	#print fname,enc
	tmp=[]
	if fname in books2:
		tmp=books2[fname]
	tmp.append(enc)
	books2[fname]=tmp

books=[]
# build list of only the books we want
for k in books2.keys():
	#print k, books2[k]
	if '' in books2[k]:                   
		books.append(dirname+k+".txt")
	elif '0' in books2[k]:
		books.append(dirname+k+"-0.txt")
	elif '8' in books2[k]:
		books.append(dirname+k+"-8.txt")
	elif '5' in books2[k]:
		books.append(dirname+k+"-5.txt")

for b in books:
	ibook = open(b, "r")
	path=b.split("/")
	fname=path[len(path)-1]
	obook = open('./'+lang+'_txt_out/'+fname, "w")
	begin=0
	count=0
	lcnt=0
	end=0
	for l in ibook.readlines():
		if "***END OF" in l or "*** END OF" in l or "End of this is COPYRIGHTED" in l or "Ende dieses" in l or "*END THE SMALL PRINT" in l or "*END*THE SMALL PRINT" in l or "Ende diese Project Gutenberg" in l or "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**" in l:
			#print "end of corpus",b
			end=1
		if begin==1 and end==0:
			lcnt+=1
			if len(l.split())<=4:
				count+=1
			else:
				obook.write(l)
		
		if "***START OF" in l or "*** START OF" in l or "**This is a COPYRIGHTED" in l or "*END THE SMALL PRINT" in l or "*END*THE SMALL PRINT" in l or "*SMALL PRINT" in l:
			#print "begin of corpus",b
			begin=1
	ibook.close()
	obook.close()
	if count > 7000 or (float(count)/lcnt)*100 > 50:
		print "skipping dict?",count,b,(float(count)/lcnt)*100
		os.remove('./'+lang+'_txt_out/'+fname)
		
	if begin != 1 or end != 1:
		print "Error finding corpus in", b, begin,end
		exit()

