#!/usr/bin/env python
###############
# data.py - holds a reference to all the data
###############

import glob
import re
import fVectors
import parallelmcca
import math
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
import cPickle as pickle
import time

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
		self.enVecs = fVectors.fVectors(langs[0])
		self.esVecs = fVectors.fVectors(langs[1])
		self.gpuFlag=0
		
	def setGPU(self):
		print "running with GPU support.."
		self.gpuFlag=1

	def runMCCA(self):
		print "in MCCA..."
		#self.esVecs.getTestVectors("german.2.part")
		tVec = self.esVecs.getTestVectors(self.langDirs[1])
		print tVec

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

		return combA, combB, legend

	def saveVecs(self):
		dirs=self.procDir+"/"+self.vecSubdir
		pickle.dump( self.enVecs, open( dirs + "/" + self.langDirs[0] + "_All.p", "wb" ) )
		#self.enVecs.saveVectors(self.procDir+"/"+self.vecSubdir)
		pickle.dump( self.esVecs, open( dirs + "/" + self.langDirs[1] + "_All.p", "wb" ) )
		#self.esVecs.saveVectors(self.procDir+"/"+self.vecSubdir)

	def loadVecs(self):
		dirs=self.procDir+"/"+self.vecSubdir
		self.enVecs = pickle.load( open( dirs + "/" + self.langDirs[0] + "_All.p", "rb" ) )
		#self.enVecs.loadVectors(self.procDir+"/"+self.vecSubdir)
		self.esVecs = pickle.load( open( dirs + "/" + self.langDirs[1] + "_All.p", "rb" ) )
		#self.esVecs.loadVectors(self.procDir+"/"+self.vecSubdir)

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
						if l == self.langDirs[0]:
							#print line.strip()
							#print "en"
							self.enVecs.buildVector(line.strip())

						else:
							#print "de"
							#print line.strip()
							self.esVecs.buildVector(line.strip())
			# clean vectors here for saving memory
			if l == self.langDirs[0]:
				self.enVecs.cleanupVector()
				self.enVecs.cleanEnglishVector(self.langDirs[1])
			else:
				self.esVecs.cleanupVector()
		
		#self.esVecs.getTestVectors("german.2.part","DICT/german.1.part")
		
	def transformVecs(self):
		print "in transformVecs().."
		g=parallelmcca.gpuProcessor()
		
		start = time.time()
		if self.gpuFlag:
			print "transforming Vectors using GPU.."
			# English
			iVec,corpSize=self.enVecs.returnVec()
			res=g.doParallelTransform(iVec,corpSize)
			self.enVecs.updateVec(res)
			
			# Foreign
			iVec,corpSize=self.esVecs.returnVec()
			res=g.doParallelTransform(iVec,corpSize)
			self.esVecs.updateVec(res)
		else:
			self.enVecs.transfromVector()
			self.esVecs.transfromVector()
		end = time.time()
		print "total time:",end-start
		
	def testVectors(self):
		print "getting test vector"
		self.esVecs.getTestVectors(self.langDirs[1])
		#self.enVecs.getTestVectors("german.2.part","DICT/german.1.part")
		if self.gpuFlag:
			print "testing on a GPU..."
		else:
			print "testing on CPU..."
			testVecs = self.esVecs.getVec()
			srcVecs = self.enVecs.getVec()
			res=[]
			print len(testVecs), len(srcVecs)
			#exit()
			
			for t in testVecs:
				best=100
				btup=(1,1)
				for s in srcVecs:
					d,c=self.getCityBlockDist(testVecs[t],srcVecs[s])
					if c>5:
						res.append((s,t,d,c))
						if d < best:
							best=d
							btup=(s,t,d,c)
				print btup
			
	def getCityBlockDist(self, S, T):
		dist=0
		missingCnt=0
		for s in S:
			if s in T:
				dist+=abs(S[s]-T[s])
			else:
				missingCnt+=1
		#print "missingCnt",missingCnt
		common= len(S)-missingCnt
		return dist,common
			
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
		return out

	def saveProcessed(self,data,fname):
		fout = open(fname+".processed", "w")
		for line in data:
			#print type(line)
			fout.write((" ".join(line)).encode('UTF-8')+"\n")


	def processFile(self,fname,lang):
		print "processing:",fname
		f = open(fname, "r")
		lines=""
		allines=[l.strip() for l in f.readlines()]
		lines1=" ".join(allines)
		try:
			lines=unicode(lines1.strip(),'UTF-8')
			print "UTF-8 succeeded"
		except:
			print "UTF-8 failed"
			try:
				lines=unicode(lines1.strip(),'iso-8859-1')
				print "iso-8859-1 succeeded"
			except:
				print "iso-8859-1 failed"
				llen=len(allines)
				for line in allines:
					#print line.strip()
					try:
						trash=unicode(line.strip(),'UTF-8')
						lines+=trash+" "
					except:
						q1+=1
						try:
							trash = unicode(line.strip(),'iso-8859-1')
							lines += trash + " "
						except:
							q4+=1
							for w in line.strip().split(" "):
								try:
									q2+=1
									trash = unicode(w,'UTF-8')
									lines += trash + " "
								except:
									#print w, " UTF-8 failed"
									try:
										q3+=1
										trash = unicode(w,'iso-8859-1')
										lines += trash + " "
										#print w, " its iso-8859-1"
									except:
										print w, " Its on UTF-8 nor ISO-8859-1 (giving up)"
					q+=1
					if q%5000==0 and q != 0:
						print (float(q)/llen)*100,"%",q1,q4,q2,q3

		#lines = unicode(self.cleanText(lines),'UTF-8')
		#lines #= unicode(lines,'UTF-8')
		if lines.find("\n")>0:
			print "WARNING!!!!",lines.find("\n"), lines[lines.find("\n")-10:lines.find("\n")+10]
			exit()
		tmp=[]

		print "tokenizing..."
		wordpunct_tokenize(lines)
		tmp+=[word_tokenize(t) for t in sent_tokenize(lines)]
		lines=tmp[:]
		tmp=[]

		print "removing punctuation and function words... "
		#TODO: move to text files, add prepostions/particles/etc
		if lang == "en":
			bad = ["he","she","it","I","you"
					,"they","we"
					,"him","her","me"
					,"them","us"
					,"his","her","my","your"
					,"their","our"
					,"hers","mine","yours"
					,"theirs","ours"
					,"a","an","the"
					,"and","either","or","but","neither","nor"
					,"in","of","to","on","for","with","by","before","after"
					,"if","then","else","thus","well","however","therefore"]
		elif lang == "es":
			bad = ["el","ella","usted","yo","tu"
					,"ellos","ellas","ustedes","nosotros","vosotros"
					,"le","la","te","me"
					,"les","las","nos","vos"
					,"su","mi","tu"
					,"nuestra","nuestro"
					,"sus","mis","tus"
					,"nuestras","nuestros"
					,"un","una","el","la"
					,"unos","unas","los","las"
					,"y","o","pero","despues"
					,"en","de","del","a","para","por","con"
					,"si"] #TODO: lookup more spanish prepositions
		elif lang == "de":
			bad = ["der","die","das","des","deren","ich","du","er","sie","es"
					,"wir","ihr","es","ein","einen","mein","dein","ihres"
					,"euer","eurer","eueres","eures","eure","euere","euerer"
					,"euerem","euerm","eurem","euren","eueren","euern","euch"
					,"deine","deins","meins","dessen","derer","denen","diesen"
					,"diesem","meiner","meinem","meinen","ihrem","ihren"]
		elif lang == "fr":
			bad = ["le","la","l'","les","un","une","des","du","de","je","me","moi","tu"
					,"te","toi","il","elle","on","lui","se","soi","nous","vous"
					,"ils","elles","leur","eux","celui","celle","ceux","celles"
					,"mon","ma","notre","nos","ton","ta","tes","votre","vos","son"
					,"sa","ses","leurs","ce","ces","cette","quel","quels","quelle"
					,"quelles"]
		else:
			fail = "you screwed up your languages... find the right stemmer yourself!! cur lang: " + lang
			exit(fail)


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
			ltmp=[]
			for w in s:
				#print w
				try:
					ltmp.append(stemmer.stem(w))
				except:
					print "cant stem this string",w
			tmp.append(ltmp)
		return tmp[:]

def removeAll(l,token):
	x = l.count(token)
	for i in range(x):
		l.remove(token)
	return l
