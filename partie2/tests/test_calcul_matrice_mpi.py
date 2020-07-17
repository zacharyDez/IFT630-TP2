import os
from unittest import TestCase

from partie2 import matrix_mult_mpi
import util.matrix_creation as mc


class TestMatrixMult(TestCase):

    def setUp(self) -> None:
        self.p1 = "5x5-1.txt"
        self.p2 = "5x5-2.txt"
        mc.create_unique_value_matrix(self.p1, 5, 5, 1)
        mc.create_unique_value_matrix(self.p2, 5, 5, 1)

    def tearDown(self) -> None:
        os.remove(self.p1)
        os.remove(self.p2)

    def test_matrix_mult_mpi_invalid_path(self) -> None:
        # params following main are parameters passed
        self.assertRaises(ValueError, matrix_mult_mpi.main, "invalid.txt", self.p1)

    def test_matrix_mult_mpi_valid_path(self) -> None:
        try:
            matrix_mult_mpi.main(self.p1, self.p2)
        except ValueError:
            self.fail("matrix_mutlt_mpi() raised ValueException unexpectedly.")
