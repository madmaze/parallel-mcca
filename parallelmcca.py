# Sample source code from the Tutorial Introduction in the documentation.

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
class gpuProcessor:
	def doParallelTransform(self, inArray, corpusSize):
		print corpusSize
		#https://github.com/compmem/cutools/blob/master/gpustruct.py
		a = numpy.array([[10.0,15.0,5.0],
				[10.0,15.0,6.0],
				[10.0,15.0,7.0],
				[10.0,15.0,5.0]],numpy.float32)
		# Total Vector count
		vecCnt=a.shape[0]
		
		# Allocate input array
		a_gpu = cuda.mem_alloc(a.size * a.dtype.itemsize)
		
		# Allocate results array Host & Device
		dest = numpy.zeros(shape=(vecCnt,1),dtype=numpy.float32)
		dest_gpu = cuda.mem_alloc(vecCnt * a.dtype.itemsize)
		
		# Copy array to GPU
		cuda.memcpy_htod(a_gpu, a)
		
		mod = SourceModule("""
		    __global__ void transformVector(float *dest, float *a, float cSize, float vCnt)
		    {
		      int tid = threadIdx.x*3;
		      int vIdx = blockIdx.x*512 + threadIdx.x;
		      // Make sure only real things run
		      if(vIdx < vCnt){
			      float k11 = a[tid+2];
			      float k12 = a[tid+1] - k11;
			      float k21 = a[tid] - k11;
			      float k22 = cSize - a[tid+1] - a[tid];
			      float C1 = k11 + k12;
			      float C2 = k21 + k22;
			      float R1 = k11 + k21;
			      float R2 = k12 + k22;
			      float N = k11 + k12 + k21 + k22;
			      
			      dest[threadIdx.x] = k11*log((k11*N)/(C1*R1)) + k12*log((k12*N)/(C1*R2)) + k21*log((k21*N)/(C2*R1)) + k22*log((k22*N)/(C2*R2));
		      }
		      
		    }
		    """)
		
		# cast cuda kernel
		func = mod.get_function("transformVector")
		
		# Make things float32s.. could probably do ints but lets not break it
		cSize=numpy.float32(corpusSize)
		vCnt=numpy.float32(vecCnt)
		
		gridx=int((vecCnt+511)/512)
		
		# Execute cuda kernel
		func(dest_gpu,a_gpu,cSize,vCnt, block=(512,1,1), grid=(gridx,1))
		
		# Return result to host
		cuda.memcpy_dtoh(dest, dest_gpu)
		
		print "Input:"
		print a
		print "Result:"
		print dest
