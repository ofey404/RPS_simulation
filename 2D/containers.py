from math import sqrt
import numpy as np
from abstract_containers import SerialNum, Lattice, SideWeight, Weight


class SerialNum2D(SerialNum):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)

    def x(self):
        return self.value()[0]

    def y(self):
        return self.value()[1]

    def __str__(self) -> str:
        return "SerialNum2D({}, {})".format(self.x(), self.y())

    def __sub__(self, other):
        x1, y1 = self.x(), self.y()
        x2, y2 = other.x(), other.y()
        return (x1 - x2, y1 - y2)


def equilateral_triangle(sn: SerialNum2D) -> tuple[float]:
    x, y = sn.value()
    return (x + y * 0.5, y * sqrt(3) / 2)


class Triangle2D(Lattice):
    __size = None
    __serial_num_to_coordination = None
    __neighbour_offsets = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))

    def __init__(self, shape=3, to_coord=equilateral_triangle) -> None:
        super().__init__(shape)
        self.__size = shape
        self.__serial_num_to_coordination = to_coord

    def __contains__(self, c: SerialNum) -> bool:
        return c.x() + c.y() < self.__size

    def size(self):
        return self.__size

    def all_serial_num(self) -> tuple[SerialNum2D]:
        return (
            SerialNum2D(i, j)
            for i in range(self.__size)
            for j in range(self.__size - i)
        )

    def to_coord(self, sn: SerialNum2D) -> tuple[float]:
        if sn not in self:
            raise Exception("SerialNum {} is not in lattice {}".format(sn, self))
        return self.__serial_num_to_coordination(sn)

    def __str__(self):
        return "Triangle2D(size={})".format(self.size())

    def neighbours(self, sn: SerialNum2D) -> tuple[SerialNum]:
        x, y = sn.value()
        non_negative = (
            (x + dx, y + dy)
            for dx, dy in self.__neighbour_offsets
            if (x + dx >= 0 and y + dy >= 0)
        )
        inside_lattice = (
            SerialNum2D(x, y) for x, y in non_negative if SerialNum2D(x, y) in self
        )
        return inside_lattice

    def neighbours_offsets(self):
        return self.__neighbour_offsets


class Triangle2DWeight(Weight):
    __weight_matrix = None

    def __init__(self, lattice: Triangle2D) -> None:
        size = lattice.size()
        self.__weight_matrix = np.zeros((size, size))

    def value(self, sn: SerialNum2D):
        x, y = sn.value()
        return self.__weight_matrix[x][y]

    def set_value(self, sn: SerialNum2D, val: float):
        x, y = sn.value()
        self.__weight_matrix[x][y] = val


class Triangle2DSideWeight(SideWeight):
    __side_weight_matrix = None
    __positive_offsets = None

    def __init__(self, lattice: Triangle2D) -> None:
        size = lattice.size()
        offsets = lattice.neighbours_offsets()
        side_per_node = int(len(offsets) / 2)
        self.__side_weight_matrix = np.zeros((size, size, side_per_node))

        self.__positive_offsets = sorted(offsets, reverse=True)[0:side_per_node]

    def value(self, lhs: SerialNum2D, rhs: SerialNum2D) -> float:
        x, y, z = self.__neighbour_to_index(lhs, rhs)
        return self.__side_weight_matrix[x][y][z]

    def set_value(self, lhs: SerialNum2D, rhs: SerialNum2D, val: float):
        x, y, z = self.__neighbour_to_index(lhs, rhs)
        self.__side_weight_matrix[x][y][z] = val

    def __neighbour_to_index(self, lhs: SerialNum2D, rhs: SerialNum2D):
        lhs, rhs = sorted([lhs, rhs], key=lambda sn: sn.value(), reverse=True)
        return (lhs.x(), lhs.y(), self.__positive_offsets.index(lhs - rhs))
