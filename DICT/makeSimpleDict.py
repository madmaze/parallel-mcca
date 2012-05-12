#!/usr/bin/env python
import glob
import random
from nltk.stem import SnowballStemmer

for fname in glob.glob("./*"):
	# chop out non input files.. aka readme
	if fname.find(".dict") > 0:
		if 1==0:
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
		else:
			print "stemming... "
			print fname
			lang=fname.split(".dict")[0].split("./")[1]
			print lang
			if lang == "spanish" or lang == "german" or lang == "french":
				Tstemmer = SnowballStemmer(lang)
			else:
				fail = "you screwed up your languages... find the right stemmer yourself!! cur lang: " + lang
				exit(fail)
			
			Sstemmer = SnowballStemmer("english")
			
			f = open(fname, "r")
			lines=[]
			for line in f.readlines():
				s,t = line.strip().split("\t")
				#print s,t
				lines.append((Sstemmer.stem(unicode(s,'UTF-8')),Tstemmer.stem(unicode(t,'UTF-8'))))
			f.close()
			f = open(lang+".all", "w")
			for l in lines:
				s,t=l
				#print s,t
				f.write(s.encode('UTF-8')+"\t"+t.encode('UTF-8')+"\n")
			f.close()
			
			f1 = open(lang+".1.part", "w")
			f2 = open(lang+".2.part", "w")
			f3 = open(lang+".3.part", "w")
			for l in lines:
				s,t=l
				if s.find("_")!=-1 or t.find("_")!=-1:
					print "skipping",s,t
				else:
					#print s,t
					r=random.randint(1,7)
					if r < 5:
						f1.write(s.encode('UTF-8')+"\t"+t.encode('UTF-8')+"\n")
					if r ==6:
						f2.write(s.encode('UTF-8')+"\t"+t.encode('UTF-8')+"\n")
					if r ==7:
						f3.write(s.encode('UTF-8')+"\t"+t.encode('UTF-8')+"\n")
			f1.close()
			f2.close()
			f3.close()
			
			
			print "done"


