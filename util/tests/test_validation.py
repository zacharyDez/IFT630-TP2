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


def test_matrix_sizes_equal() -> None:
    p1 = "matrix1.txt"
    p2 = "matrix2.txt"
    val = 1
    size = 5
    mc.create_unique_value_matrix(path=p1, num_cols=size, num_rows=size, val=val)
    mc.create_unique_value_matrix(path=p2, num_cols=size, num_rows=size, val=val)

    assert mv.is_matrix_sizes_equal(p1, p2) is True

    os.remove(p1)
    os.remove(p2)


def test_matrix_cols_number_not_equal() -> None:
    p1 = "matrix1.txt"
    p2 = "matrix2.txt"
    val = 1
    size1 = 5
    size2 = 4
    mc.create_unique_value_matrix(path=p1, num_cols=size1, num_rows=size1, val=val)
    mc.create_unique_value_matrix(path=p2, num_cols=size1, num_rows=size2, val=val)

    assert mv.is_matrix_sizes_equal(p1, p2) is False

    os.remove(p1)
    os.remove(p2)


def test_matrix_cols_number_not_equal() -> None:
    p1 = "matrix1.txt"
    p2 = "matrix2.txt"
    val = 1
    size1 = 5
    size2 = 4
    mc.create_unique_value_matrix(path=p1, num_cols=size2, num_rows=size1, val=val)
    mc.create_unique_value_matrix(path=p2, num_cols=size1, num_rows=size1, val=val)

    assert mv.is_matrix_sizes_equal(p1, p2) is False

    os.remove(p1)
    os.remove(p2)
