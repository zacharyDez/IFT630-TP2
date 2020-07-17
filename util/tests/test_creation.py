import os

from util import matrix_creation as mc


def test_create_matrix_unique_value() -> None:
    p = "matrix1.txt"
    val = 1
    size = 5
    mc.create_unique_value_matrix(path=p, num_cols=size, num_rows=size, val=val)

    with open(p) as f:
        exp_line = [val for x in range(0, size)]
        for line in f.readlines():
            assert [int(x) for x in line.split()] == exp_line

    os.remove(p)
