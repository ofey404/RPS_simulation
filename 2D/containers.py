from math import sqrt
from abstract_containers import SerialNum, Lattice, SideWeight, Weight


class SerialNum2D(SerialNum):
    def __init__(self, *val) -> None:
        if len(val) != 2:
            raise Exception("len(val) = {}, should be 2".format(len(val)))
        super().__init__(*val)

    def x(self):
        return self.value()[0]

    def y(self):
        return self.value()[1]

    def __str__(self) -> str:
        return "SerialNum2D({}, {})".format(self.x(), self.y())


def equilateral_triangle(sn: SerialNum2D) -> tuple[float]:
    x, y = sn.value()
    return (x + y * 0.5, y * sqrt(3) / 2)


class Triangle2D(Lattice):
    __size = None
    __serial_num_to_coordination = None
    __neighbour_offsets = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))

    def __init__(self, *shape, to_coord=equilateral_triangle) -> None:
        if len(shape) != 1:
            raise Exception("len(shape) = {}, should be 1".format(len(shape)))
        super().__init__(*shape)
        self.__size = shape[0]
        self.__serial_num_to_coordination = to_coord

    def __contains__(self, c: SerialNum) -> bool:
        return c.x() + c.y() < self.__size

    def size(self):
        return self.__size

    def all_serial_num(self) -> tuple[SerialNum2D]:
        return ((i, j) for i in range(self.__size) for j in range(self.__size - i))

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
        inside = (
            SerialNum2D(x, y) for x, y in non_negative if SerialNum2D(x, y) in self
        )
        return inside


class Triangle2DWeight(Weight):
    __lattice = None

    def __init__(self, lattice: Triangle2D) -> None:
        self.__lattice = lattice
