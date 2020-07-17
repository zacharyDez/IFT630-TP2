import sys
import math
from mpi4py import MPI
import numpy as np

import util.matrix_validation as mv
import util.matrix_read as mr
import util.matrix_creation as mc


def divide_array(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def main(dest_path: str, m1_path: str, m2_path: str) -> None:
    if not mv.is_matrix_path_exist(m1_path) or not mv.is_matrix_path_exist(m2_path):
        raise ValueError(f"{m1_path} or {m2_path} does not exist.")

    if not mv.is_matrix_sizes_equal(m1_path, m2_path):
        raise ValueError(f"{m1_path} or {m2_path} do not have matching sizes.")

    # exceptions passed, initialisation for parallel processing
    # Object for processing space
    comm = MPI.COMM_WORLD
    # size of processing space, represents number of working entities
    size = comm.Get_size()
    # Rank of current process, used as unique identifier
    rank = comm.Get_rank()

    # defined receive buffer based on size of matrice and number of processes
    dim = mr.get_matrix_size(m1_path)
    num_elements_per_process = 10 #int(np.ceil(dim[0] * dim[0] / size - 1))

    # Administrator process
    if rank == 0:
        m1_data = [val for val in mr.get_matrix_val_gen(m1_path)]
        m2_data = [val for val in mr.get_matrix_val_gen(m2_path)]

        merge_data = [(m1_data[i], m2_data[i]) for i in range(len(m1_data))]

    else:
        # must reference data to avoid reference before assignment in workers
        merge_data = None

    # Worker process
    receive_buffer = np.empty(num_elements_per_process, dtype='d')
    comm.Scatter(merge_data, receive_buffer, root=0)

    print(f"Process {rank} received: {receive_buffer}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    # TODO: fix being able to call with more than two processes
    #  Example command that works for now: mpiexec -n 2 python matrix_mult_mpi.py result.txt m1.txt m2.txt
