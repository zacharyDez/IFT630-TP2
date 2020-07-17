import os

from util import matrix_validation as mv
from util import matrix_creation as mc


def create_matrix_file(path: str) -> None:
    with open(path, "w+") as f:
        f.close()


def test_validate_paths_matrix_passes() -> None:
    p1 = "matrix1.txt"
    p2 = "matrix2.txt"
    create_matrix_file(p1)
    create_matrix_file(p2)

    assert mv.is_matrix_path_exist(p1)
    assert mv.is_matrix_path_exist(p2)

    os.remove(p1)
    os.remove(p2)


def test_validate_paths_fails() -> None:
    p1 = "matrix1.txt"
    p2 = "matrix2.txt"

    create_matrix_file(p1)

    assert mv.is_matrix_path_exist(p1) is True
    assert mv.is_matrix_path_exist(p2) is False

    os.remove(p1)


def test_create_matrice_unique_value() -> None:
    p = "matrice1.txt"
    val = 1
    size = 5
    mc.create_unique_value_matrix(path=p, num_cols=size, num_rows=size, val=val)

    with open(p) as f:
        exp_line = [val for x in range(0, size)]
        for line in f.readlines():
            assert [int(x) for x in line.split()] == exp_line
