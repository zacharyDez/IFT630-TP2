import os
from unittest import TestCase

from util import matrix_validation as mv
from util import matrix_creation as mc


class TestMatrixPathValidation(TestCase):

    def setUp(self):
        self.p1 = "matrix1.txt"
        self.p2 = "matrix2.txt"

    def tearDown(self):
        os.remove(self.p1)

        try:
            os.remove(self.p2)
        except FileNotFoundError:
            pass

    @staticmethod
    def create_matrix_file(path: str) -> None:
        with open(path, "w+") as f:
            f.close()

    def test_validate_paths_matrix_passes(self) -> None:
        self.create_matrix_file(self.p1)
        self.create_matrix_file(self.p2)

        assert mv.is_matrix_path_exist(self.p1)
        assert mv.is_matrix_path_exist(self.p2)

    def test_validate_paths_fails(self) -> None:
        self.create_matrix_file(self.p1)

        assert mv.is_matrix_path_exist(self.p1) is True
        assert mv.is_matrix_path_exist(self.p2) is False


class TestMatrixSizeValidation(TestCase):

    def setUp(self):
        self.val = 1
        self.p1 = "matrix1.txt"
        self.p2 = "matrix2.txt"

    def tearDown(self):
        os.remove(self.p1)
        os.remove(self.p2)

    def test_matrix_sizes_equal(self) -> None:
        mc.create_unique_value_matrix(path=self.p1, num_cols=5, num_rows=5, val=self.val)
        mc.create_unique_value_matrix(path=self.p2, num_cols=5, num_rows=5, val=self.val)

        assert mv.is_matrix_sizes_equal(self.p1, self.p2) is True

    def test_matrix_cols_number_not_equal(self) -> None:
        mc.create_unique_value_matrix(path=self.p1, num_cols=5, num_rows=5, val=self.val)
        mc.create_unique_value_matrix(path=self.p2, num_cols=5, num_rows=4, val=self.val)

        assert mv.is_matrix_sizes_equal(self.p1, self.p2) is False

    def test_matrix_cols_number_not_equal(self) -> None:
        mc.create_unique_value_matrix(path=self.p1, num_cols=4, num_rows=5, val=self.val)
        mc.create_unique_value_matrix(path=self.p2, num_cols=5, num_rows=5, val=self.val)

        assert mv.is_matrix_sizes_equal(self.p1, self.p2) is False
