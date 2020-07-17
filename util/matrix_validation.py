import os


def is_matrix_path_exist(path: str) -> bool:
    if os.path.exists(path):
        return True

    return False


def is_matrix_sizes_equal(matrix1_path: str, matrix2_path) -> bool:
    # with (open(matrix1_path), open(matrix2_path)) as (m1, m2):
    #     print("yes")
    return False
