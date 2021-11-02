from __future__ import annotations
from math import sqrt
import numpy as np
from abstract_containers import Edge, SerialNum, Lattice, EdgeWeight, Weight

TRIANGLE_2D_NEIGHBOUR_OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))

# REFACTOR: More elegant way to map neighbour offset to index.
POSITIVE_OFFSETS = sorted(TRIANGLE_2D_NEIGHBOUR_OFFSETS, reverse=True)[
    0 : int(len(TRIANGLE_2D_NEIGHBOUR_OFFSETS))
]


def equilateral_triangle(sn: SerialNum2D) -> tuple[float]:
    x, y = sn.value()
    return (x + y * 0.5, y * sqrt(3) / 2)


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


class Triangle2DEdgeWeight(EdgeWeight):
    __side_weight_matrix = None

    def __init__(self, lattice: Triangle2D) -> None:
        size = lattice.size()
        self.__side_weight_matrix = np.zeros((size, size, len(POSITIVE_OFFSETS)))

    def value(self, edge: UndirectedEdge2D) -> float:
        x, y, z = self.__neighbour_to_index(edge)
        return self.__side_weight_matrix[x][y][z]

    def set_value(self, edge: UndirectedEdge2D, val: float):
        x, y, z = self.__neighbour_to_index(edge)
        self.__side_weight_matrix[x][y][z] = val

    def __neighbour_to_index(self, edge: UndirectedEdge2D):
        lhs, rhs = sorted([edge.start(), edge.end()], reverse=True)
        return (lhs.x(), lhs.y(), POSITIVE_OFFSETS.index(lhs - rhs))


class Triangle2D(Lattice):
    __size = None
    __serial_num_to_coordination = None

    def __init__(self, shape=3, to_coord=equilateral_triangle) -> None:
        super().__init__(shape)
        self.__size = shape
        self.__serial_num_to_coordination = to_coord

    def __contains__(self, c: SerialNum) -> bool:
        return c.x() + c.y() < self.__size

    def __str__(self):
        return "Triangle2D(size={})".format(self.size())

    def size(self):
        return self.__size

    def all_serial_num(self) -> tuple[SerialNum2D]:
        return (
            SerialNum2D(i, j)
            for i in range(self.__size)
            for j in range(self.__size - i)
        )

    def all_edges(self) -> tuple[UndirectedEdge2D]:
        all_include_duplicated = (
            UndirectedEdge2D(sn, neighbour)
            for sn in self.all_serial_num()
            for neighbour in self.neighbours(sn)
        )
        return tuple(set(all_include_duplicated))

    def to_coord(self, sn: SerialNum2D) -> tuple[float]:
        if sn not in self:
            raise Exception("SerialNum {} is not in lattice {}".format(sn, self))
        return self.__serial_num_to_coordination(sn)

    def neighbours(self, sn: SerialNum2D) -> tuple[SerialNum]:
        x, y = sn.value()
        non_negative_neighbours = (
            (x + dx, y + dy)
            for dx, dy in TRIANGLE_2D_NEIGHBOUR_OFFSETS
            if (x + dx >= 0 and y + dy >= 0)
        )
        filter_inside_lattice = (
            SerialNum2D(x, y) for x, y in non_negative_neighbours if SerialNum2D(x, y) in self
        )
        return filter_inside_lattice


class UndirectedEdge2D(Edge):
    def __eq__(self, other: UndirectedEdge2D):
        return (self.start() == other.start() and self.end() == other.end()) or (
            self.start() == other.end() and self.end() == other.start()
        )

    def __hash__(self):
        return hash(tuple(sorted((self.start(), self.end()))))


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

    def __hash__(self) -> int:
        return self.value().__hash__()

    def __eq__(self, other: SerialNum2D):
        return self.value() == other.value()

    def __lt__(self, other: SerialNum2D):
        return self.value() < other.value()
