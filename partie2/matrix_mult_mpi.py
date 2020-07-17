import util.matrix_validation as mv


def main(m1_path: str, m2_path: str) -> None:
    if not mv.is_matrix_path_exist(m1_path) or not mv.is_matrix_path_exist(m2_path):
        raise ValueError(f"{m1_path} or {m2_path} does not exist.")

    if not mv.is_matrix_sizes_equal(m1_path, m2_path):
        raise ValueError(f"{m1_path} or {m2_path} do not have matching sizes.")