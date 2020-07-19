import sys

from mpi4py import MPI

from util.matrix_read import get_matrix_val_gen
import util.matrix_validation as mv


def divide_array(seq: list, num: int) -> list:
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

    comm = MPI.COMM_WORLD
    num_process = size = comm.Get_size()  # new: gives number of ranks in comm
    rank = comm.Get_rank()

    # default if rank is not 0
    split_merge_data = None

    # process is administrator
    if rank == 0:
        m1_data = [val for val in get_matrix_val_gen(m1_path)]
        m2_data = [val for val in get_matrix_val_gen(m2_path)]
        merge_data = [(m1_data[i], m2_data[i]) for i in range(len(m1_data))]

        ave, res = divmod(len(merge_data), num_process)
        split_merge_data = divide_array(merge_data, num_process - 1)

        for i in range(num_process - 1):
            req = comm.isend(split_merge_data[i], dest=i + 1)
            req.wait()

        # TODO: writes contents
        with open(dest_path, "w+") as f:
            pass

    # process is a worker
    else:
        # Réception de données par appel bloquant.
        req = comm.irecv(source=0)
        data = req.wait()
        result = [mv[0] * mv[1] for mv in data]
        print(f"Process {rank} received: {result}")

    comm.Barrier()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
