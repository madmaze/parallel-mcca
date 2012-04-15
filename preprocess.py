#!/usr/bin/env python
import glob

def main(dataDir, langDirs):
	for l in langDirs:
		for f in glob.glob(dataDir + "/" + l + "/*"):
			# chop out non input files.. aka readme
			if f.find(".txt") > 0:
				print f

if __name__ == "__main__":
	langs=["en","es"]
	inputDir="./DATA"
	main(inputDir,langs)