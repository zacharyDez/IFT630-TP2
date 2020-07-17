from mpi4py import MPI
import math

from util.matrix_read import get_matrix_val_gen


def divide_array(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


comm = MPI.COMM_WORLD
num_process = size = comm.Get_size()  # new: gives number of ranks in comm
rank = comm.Get_rank()

# default if rank is not 0
split_merge_data = None

if rank == 0:
    m1_data = [val for val in get_matrix_val_gen("m1.txt")]
    m2_data = [val for val in get_matrix_val_gen("m2.txt")]
    merge_data = [(m1_data[i], m2_data[i]) for i in range(len(m1_data))]

    ave, res = divmod(len(merge_data), num_process)
    split_merge_data = divide_array(merge_data, num_process - 1)

    for i in range(num_process-1):
        req = comm.isend(split_merge_data[i], dest=i+1)
        req.wait()
# process is a worker
else:
    # Réception de données par appel bloquant.
    req = comm.irecv(source=0)
    data = req.wait()
    result = [mv[0]*mv[1] for mv in data]
    print(f"Process {rank} received: {result}")

comm.Barrier()