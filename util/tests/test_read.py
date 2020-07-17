import os

from util import matrix_read as mr
from util import matrix_creation as mc


def test_yield_matrices_values() -> None:
    mc.create_unique_value_matrix("m1.txt", 5, 5, 1)

    actual_vals = [val for val in mr.getMatrixValGen("m1.txt")]

    # getMatrixVal returns a float generator
    expected_vals = [float(1) for x in range(0, 5 * 5)]

    assert actual_vals == expected_vals and len(actual_vals) == 25

    os.remove("m1.txt")
