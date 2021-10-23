import unittest
import random
from math import sqrt
from containers import (
    UndirectedEdge2D,
    equilateral_triangle,
    SerialNum2D,
    Triangle2D,
    Triangle2DWeight,
    Triangle2DEdgeWeight,
)


def almost_equal_points(testcase, lhs, rhs):
    testcase.assertAlmostEqual(lhs[0], rhs[0], places=4)
    testcase.assertAlmostEqual(lhs[1], rhs[1], places=4)


def serial_nums_to_tuples(sns: tuple[SerialNum2D]):
    return (sn.value() for sn in sns)


def assert_serial_nums_eq_tuples(testcase, sns: tuple[SerialNum2D], tups: tuple[int]):
    testcase.assertCountEqual(serial_nums_to_tuples(sns), tups)


class TestTriangle2DWeight(unittest.TestCase):
    def setUp(self) -> None:
        self.size_3_lattice = Triangle2D(3)
        self.weight = Triangle2DWeight(self.size_3_lattice)
        self.all_serial_num = self.size_3_lattice.all_serial_num()

    def test_default_value(self):
        for sn in self.all_serial_num:
            self.__is_default_val(sn)

    def __is_default_val(self, sn: SerialNum2D):
        self.assertEqual(0, self.weight.value(sn))

    def test_set_value_all_sn(self):
        for sn in self.all_serial_num:
            self.__is_default_val(sn)
            self.__set_random_value(sn)

    def __set_random_value(self, sn: SerialNum2D):
        rnd = random.random()
        self.weight.set_value(sn, rnd)
        self.assertEqual(rnd, self.weight.value(sn))


class TestTriangle2DEdgeWeight(unittest.TestCase):
    def setUp(self) -> None:
        self.size_4_lattice = Triangle2D(4)
        self.side_weight = Triangle2DEdgeWeight(self.size_4_lattice)
        self.all_serial_num = self.size_4_lattice.all_serial_num()

    def test_default_value(self):
        edges = self.size_4_lattice.all_edges()
        for e in edges:
            self.__is_default_val(e)

    def __is_default_val(self, edge: UndirectedEdge2D):
        self.assertEqual(0, self.side_weight.value(edge))

    def test_set_value(self):
        edges = self.size_4_lattice.all_edges()
        for e in edges:
            self.__is_default_val(e)
            rnd = random.random()
            self.side_weight.set_value(e, rnd)
            self.assertEqual(rnd, self.side_weight.value(e))


class TestTriangle2D(unittest.TestCase):
    def setUp(self) -> None:
        self.size_3 = Triangle2D(3)

    def test_size(self):
        self.assertEqual(self.size_3.size(), 3)

    def test_in(self):
        self.assertTrue(SerialNum2D(0, 0) in self.size_3)
        self.assertTrue(SerialNum2D(2, 0) in self.size_3)

        self.assertFalse(SerialNum2D(2, 1) in self.size_3)

    def test_all_serial_num(self):
        assert_serial_nums_eq_tuples(
            self,
            self.size_3.all_serial_num(),
            ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)),
        )

    def test_all_edges(self):
        size_2 = Triangle2D(2)
        s00 = SerialNum2D(0, 0)
        s10 = SerialNum2D(1, 0)
        s01 = SerialNum2D(0, 1)
        e0 = UndirectedEdge2D(s00, s10)
        e1 = UndirectedEdge2D(s00, s01)
        e2 = UndirectedEdge2D(s01, s10)

        self.assertCountEqual((e0, e1, e2), size_2.all_edges())

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
        assert_serial_nums_eq_tuples(
            self,
            self.size_3.neighbours(SerialNum2D(1, 1)),
            ((1, 0), (0, 1), (0, 2), (2, 0)),
        )
        assert_serial_nums_eq_tuples(
            self,
            self.size_3.neighbours(SerialNum2D(0, 0)),
            ((1, 0), (0, 1)),
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

    def test_sub(self):
        s1 = SerialNum2D(0, 0)
        s2 = SerialNum2D(1, 2)
        self.assertEqual(s2 - s1, (1, 2))

    def test_eq(self):
        self.assertEqual(SerialNum2D(1, 1), SerialNum2D(1, 1))
        self.assertNotEqual(SerialNum2D(0, 0), SerialNum2D(1, 1))

    def test_lt(self):
        self.assertEqual((1, 0) < (0, 0), SerialNum2D(1, 0) < SerialNum2D(0, 0))

    def test_hash(self):
        self.assertEqual(hash(SerialNum2D(1, 1)), hash(SerialNum2D(1, 1)))
        self.assertNotEqual(hash(SerialNum2D(0, 0)), hash(SerialNum2D(1, 1)))


class TestUndirectedEdge2D(unittest.TestCase):
    def setUp(self) -> None:
        self.s0 = SerialNum2D(0, 0)
        self.s1 = SerialNum2D(1, 1)
        self.s2 = SerialNum2D(2, 2)

        self.e01 = UndirectedEdge2D(self.s0, self.s1)
        self.e10 = UndirectedEdge2D(self.s1, self.s0)
        self.e12 = UndirectedEdge2D(self.s1, self.s2)

    def test_eq(self):
        self.assertEqual(self.e01, self.e01)
        self.assertEqual(self.e01, self.e10)
        self.assertNotEqual(self.e01, self.e12)

    def test_hash(self):
        self.assertEqual(hash(self.e10), hash(self.e01))
        self.assertNotEqual(hash(self.e01), hash(self.e12))


class TestHelperFunctions(unittest.TestCase):
    def test_equilateral_triangle(self):
        almost_equal_points(self, (0, 0), equilateral_triangle(SerialNum2D(0, 0)))
        almost_equal_points(self, (1, 0), equilateral_triangle(SerialNum2D(1, 0)))
        almost_equal_points(
            self, (1.5, sqrt(3) / 2), equilateral_triangle(SerialNum2D(1, 1))
        )


if __name__ == "__main__":
    unittest.main()
