#!/usr/bin/env python
import data
import optparse
import parallelmcca


if __name__ == "__main__":
	optparser = optparse.OptionParser()
	optparser.add_option("-i", "--dataDir", dest="datadir", default="DATA", type="string", help="Dir for lang input files (default='DATA')")
	optparser.add_option("-o", "--procDir", dest="procDir", default="PROCESSED", type="string", help="Dir for storing Processing files (default='PROCESSED')")
	optparser.add_option("-l", "--langs", dest="langs", default="en,de", type="string", help="Languages (default='en,es')")
	optparser.add_option("-p", "--preprocess", action="store_true", dest="preproc_flag", default=False, help="Run preprocessing")
	optparser.add_option("-r", "--run", action="store_true", dest="run_flag", default=False, help="Run MCCA")
	optparser.add_option("-s", "--gpu", action="store_true", dest="gpu_flag", default=False, help="Run MCCA")
	optparser.add_option("-t", "--transformVecs", action="store_true", dest="trans_flag", default=False, help="Run MCCA")
	optparser.add_option("-g", "--genVectors", action="store_true", dest="genV_flag", default=False, help="Generate Vectors")
	(opts,args) = optparser.parse_args()
	D = data.data(opts.datadir,opts.langs.split(","),opts.procDir)
	print "Options set:"
	print opts
	print args
	if opts.gpu_flag:
		print " Setting GPU support..."
		D.setGPU()
		
	if opts.preproc_flag:
		print " Entering PreProcessing step..."
		D.preprocess()
	elif opts.genV_flag:
		print " Entering Vector Generation..."
		D.genVectors()
		D.saveVecs()
	elif opts.trans_flag:
		print " Entering Vector Transformation..."
		D.loadVecs()
		D.transformVecs()
		D.testVectors()
		#D.saveVecs()
	elif opts.run_flag:
		print " Entering MCCA calculation..."
		D.loadVecs()
		D.testVectors()
	else:
		print "No option selected..."
		
