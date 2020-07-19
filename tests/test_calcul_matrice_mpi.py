import os
import time
from unittest import TestCase

import matrix_mult_mpi
import util.matrix_creation as mc
import util.matrix_read as mr


# TODO: must be able to call matrix_mult_mpi using mpi.
#  Not sure how to design tests with that other than doign integration tests
#  Example command that works for now: mpiexec -n 2 python matrix_mult_mpi.py

class TestMatrixMult(TestCase):

    def setUp(self) -> None:
        self.p1 = "5x5-3.txt"
        self.p2 = "5x5-2.txt"
        self.p3 = "5x6-1.txt"
        mc.create_unique_value_matrix(self.p1, 5, 5, 3)
        mc.create_unique_value_matrix(self.p2, 5, 5, 2)
        mc.create_unique_value_matrix(self.p3, 5, 6, 1)

    def tearDown(self) -> None:
        os.remove(self.p1)
        os.remove(self.p2)
        os.remove("5x6-1.txt")

    def test_invalid_path_exception(self) -> None:
        # params following main are parameters passed
        self.assertRaises(ValueError, matrix_mult_mpi.main, "wont_write.txt", "invalid.txt", self.p1)

    def test_matrices_size_exception(self) -> None:
        self.assertRaises(ValueError, matrix_mult_mpi.main, "wont_write.txt", self.p1, self.p3)

    def test_matrix_mult_result_correct(self) -> None:
        os.system(f"mpiexec -n 4 python matrix_mult_mpi.py result.txt {self.p1} {self.p2}")

        actual_values = [val for val in mr.get_matrix_val_gen("result.txt")]
        expected_values = [2 * 3 for x in range(0, 5 * 5)]

        assert actual_values == expected_values

        os.remove("result.txt")