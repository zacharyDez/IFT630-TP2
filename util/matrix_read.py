from typing import Generator
from typing import Tuple


def get_matrix_val_gen(path: str) -> Generator[float, None, None]:
    # returns float generator
    # float used as int is subset of type
    with open(path) as f:
        for row in f:
            for value in row.split():
                yield float(value)

        f.close()


def get_matrix_size(path: str) -> Tuple[int, int]:
    with open(path) as f:
        num_cols = len(f.readline().split())
        # previous readline removes first row
        num_rows = len(f.readlines()) + 1

    return num_rows, num_cols
