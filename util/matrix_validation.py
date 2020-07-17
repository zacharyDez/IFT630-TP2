import os

import util.matrix_read as mr


def is_matrix_path_exist(path: str) -> bool:
    if os.path.exists(path):
        return True

    return False


def is_matrix_sizes_equal(matrix1_path: str, matrix2_path) -> bool:
    if mr.get_matrix_size(matrix1_path) != mr.get_matrix_size(matrix2_path):
        return False

    return True
