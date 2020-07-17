import os
from unittest import TestCase

from partie2 import matrix_mult_mpi
import util.matrix_creation as mc


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

    def test_invalid_path_exception(self) -> None:
        # params following main are parameters passed
        self.assertRaises(ValueError, matrix_mult_mpi.main, "invalid.txt", self.p1)

    def test_valid_path_no_exception(self) -> None:
        try:
            matrix_mult_mpi.main(self.p1, self.p2)
        except ValueError:
            self.fail("matrix_mutlt_mpi() raised ValueException unexpectedly.")

    def test_matrices_size_exception(self) -> None:
        self.assertRaises(ValueError, matrix_mult_mpi.main, self.p1, self.p3)
