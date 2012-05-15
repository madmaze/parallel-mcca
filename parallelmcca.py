# Sample source code from the Tutorial Introduction in the documentation.

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
class gpuProcessor:
	def doParallelTransform(self,inArray):
		#https://github.com/compmem/cutools/blob/master/gpustruct.py
		a = numpy.array([[10.0,15.0,5.0],
				[10.0,15.0,6.0],
				[10.0,15.0,7.0],
				[10.0,15.0,5.0]],numpy.float32)
		itemCnt=a.shape[0]
		
		# Allocate input array
		a_gpu = cuda.mem_alloc(a.size * a.dtype.itemsize)
		# Allocate results array Host & Device
		dest = numpy.zeros(shape=(itemCnt,1),dtype=numpy.float32)
		dest_gpu = cuda.mem_alloc(itemCnt * a.dtype.itemsize)
		
		
		cuda.memcpy_htod(a_gpu, a)
		
		mod = SourceModule("""
		    __global__ void doublify(float *dest, float *a, float cSize)
		    {
		      int tid = threadIdx.x*3;

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
		    """)
		
		func = mod.get_function("doublify")
		cSize=numpy.float32(1450)
		func(dest_gpu,a_gpu,cSize, block=(4,1,1))
		
		#a_doubled = numpy.empty_like(a)
		cuda.memcpy_dtoh(dest, dest_gpu)
		
		print "original array:"
		print a
		print "doubled with kernel:"
		print dest
		
		# alternate kernel invocation -------------------------------------------------
		'''
		func(cuda.InOut(a), block=(4, 4, 1))
		print "doubled with InOut:"
		print a
		
		# part 2 ----------------------------------------------------------------------
		
		import pycuda.gpuarray as gpuarray
		a_gpu = gpuarray.to_gpu(numpy.random.randn(4,4).astype(numpy.float32))
		a_doubled = (2*a_gpu).get()
		
		print "original array:"
		print a_gpu
		print "doubled with gpuarray:"
		print a_doubled
		'''