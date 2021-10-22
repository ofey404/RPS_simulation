import unittest
from math import sqrt
from containers import SerialNum2D, Triangle2D, equilateral_triangle


def almost_equal_points(testcase, lhs, rhs):
    testcase.assertAlmostEqual(lhs[0], rhs[0], places=4)
    testcase.assertAlmostEqual(lhs[1], rhs[1], places=4)


class TestFunctions(unittest.TestCase):
    # FIXME: Duplicate code

    def test_equilateral_triangle(self):
        almost_equal_points(self, (0, 0), equilateral_triangle(SerialNum2D(0, 0)))
        almost_equal_points(self, (1, 0), equilateral_triangle(SerialNum2D(1, 0)))
        almost_equal_points(
            self, (1.5, sqrt(3) / 2), equilateral_triangle(SerialNum2D(1, 1))
        )


class TestSerialNum2D(unittest.TestCase):
    def test_init_not_negative(self):
        with self.assertRaises(Exception):
            SerialNum2D(-1, 2)

    def test_init_length_2(self):
        with self.assertRaises(Exception):
            SerialNum2D(1, 2, 3)

        with self.assertRaises(Exception):
            SerialNum2D(1)

    def test_xy(self):
        s = SerialNum2D(1, 2)
        self.assertEqual(s.x(), 1)
        self.assertEqual(s.y(), 2)


class TestTriangle2D(unittest.TestCase):
    def test_init_length_1(self):
        with self.assertRaises(Exception):
            Triangle2D()

        with self.assertRaises(Exception):
            Triangle2D(1, 2)

    def setUp(self) -> None:
        self.size_3 = Triangle2D(3)

    def test_size(self):
        self.assertEqual(self.size_3.size(), 3)

    def test_in(self):
        self.assertTrue(SerialNum2D(0, 0) in self.size_3)
        self.assertTrue(SerialNum2D(2, 0) in self.size_3)

        self.assertFalse(SerialNum2D(2, 1) in self.size_3)

    def test_all_serial_num(self):
        self.assertCountEqual(
            self.size_3.all_serial_num(),
            ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)),
        )

    # FIXME: Duplicate code
    def almost_equal_points(self, lhs, rhs):
        self.assertAlmostEqual(lhs[0], rhs[0], places=4)
        self.assertAlmostEqual(lhs[1], rhs[1], places=4)

    def test_to_coord(self):
        almost_equal_points(self, (0, 0), self.size_3.to_coord(SerialNum2D(0, 0)))
        almost_equal_points(self, (1, 0), self.size_3.to_coord(SerialNum2D(1, 0)))
        almost_equal_points(
            self, (1.5, sqrt(3) / 2), self.size_3.to_coord(SerialNum2D(1, 1))
        )

    def test_to_coord_sn_not_in_lattice(self):
        with self.assertRaises(Exception):
            self.size_3.to_coord(SerialNum2D(2, 2))

    def test_neighbours(self):
        self.assertCountEqual(
            (
                neighbours.value()
                for neighbours in self.size_3.neighbours(SerialNum2D(1, 1))
            ),
            ((1, 0), (0, 1), (0, 2), (2, 0)),
        )
        self.assertCountEqual(
            (
                neighbours.value()
                for neighbours in self.size_3.neighbours(SerialNum2D(0, 0))
            ),
            ((1, 0), (0, 1)),
        )


if __name__ == "__main__":
    unittest.main()
