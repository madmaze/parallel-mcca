#!/usr/bin/env python
import glob
import random

for fname in glob.glob("./*"):
	# chop out non input files.. aka readme
	if fname.find(".fulldict") > 0:
		f = open(fname, "r")
		print fname
		lines=""
		entries={}
		ent=[]
		q=0
		for line in f.readlines():
			bit1=line.split("\t")[0].strip()
			bit2=line.split("\t")[1].strip()
			if(bit1 in entries):
				ent=entries[bit1]
				ent.append(bit2)
				entries[bit1]=ent  
			else:
				ent=[]
				ent.append(bit2)
				entries[bit1]=ent
			q+=1
			if q%500==0:
				print q
		f.close()
		f = open(fname.split(".full")[0]+".dict","w")
		for k in entries:
			l=len(entries[k])
			l=random.randint(1,l)
			f.write(k+"\t"+entries[k][l-1]+"\n")
		f.close()
		print len(entries.keys())

print "done"


