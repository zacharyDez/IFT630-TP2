import pyopencl as cl
import numpy as np
import os
import math


def read_file(filename):

    file = open(filename, 'r')
    matrix_len = file.readline()

    count = 0

    for i in matrix_len.strip():
        if i != " ":
            count += 1
    file.close()

    file = open(filename, 'r')
    matrix = file.read().strip()

    matrix = matrix.replace(" ", "")
    matrix = matrix.replace("\n", "")

    file.close()

    l = []

    for i in matrix:
        l.append(i)
    
    final_matrix = np.array(l)
    final_matrix = final_matrix.astype(np.float)

    return final_matrix


def main():

    os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
    os.environ['PYOPENCL_CTX'] = '1'

    a = read_file("./matrice1")
    b = read_file("./matrice2")
    c = np.zeros(len(a), dtype=np.float)

    size = math.sqrt(len(a))

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

    prg = cl.Program(ctx, 
            """
				void multiply(int n, __global float *a, __global float *b, __global float *c) {						
			   	int gid1 = get_global_id(0);																	
			   	int gid2 = get_global_id(1);																	
					float value = 0;																				
               	for(int k = 0; k < n; ++k)																		
					{																								
						float elementA = A[gid2 * n + k];															
						float elementB = B[k * n + gid1];																
						value += elementA * elementB																
					}																									
					C[gid2 * n + gid1] = value;																		
				}																									
            """).build()
    

    prg.multiply(queue, c.shape, None, size, a_buf, b_buf, c_buf)
        
    a_mul_b = np.empty_like(c)
    cl.enqueue_copy(queue, a_mul_b, c_buf)

    print(a_mul_b.reshape(size, size))

main()