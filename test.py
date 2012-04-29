#!/usr/bin/env python
import data
import optparse


if __name__ == "__main__":
	optparser = optparse.OptionParser()
	optparser.add_option("-i", "--datadir", dest="datadir", default="DATA", type="string", help="Dir for lang input files (default='DATA')")
	optparser.add_option("-l", "--langs", dest="langs", default="en,es", type="string", help="Languages (default='en,es')")
	optparser.add_option("-p", "--preprocess", action="store_true", dest="preproc_flag", default=False, help="Run preprocessing")
	optparser.add_option("-r", "--run", action="store_true", dest="run_flag", default=False, help="Run MCCA")
	(opts,args) = optparser.parse_args()
	D = data.data('DATA',["en","es"])
	print "Options set:"
	print opts
	print args
	if opts.preproc_flag:
		print " Entering PreProcessing step..."
		D.preprocess()
	elif opts.run_flag:
		print " Entering MCCA calculation..."
		D.runMCCA()
	else:
		print "No option selected..."
		
