import os


def is_matrix_path_exist(path: str) -> bool:
    if os.path.exists(path):
        return True

    return False


def is_matrix_sizes_equal(matrix1_path: str, matrix2_path) -> bool:
    with open(matrix1_path) as m1, open(matrix2_path) as m2:
        m1_vals = m1.readlines()
        m2_vals = m2.readlines()

        if len(m1_vals) != len(m2_vals):
            return False

        for i in range(0, len(m1_vals) - 1):
            if len(m1_vals[i]) != len(m2_vals[i]):
                return False

    return True
