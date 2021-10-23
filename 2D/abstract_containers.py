from __future__ import annotations


def all_positive(*val):
    for i, v in enumerate(val):
        if v < 0:
            raise Exception(
                "all fields of serial number should be positive, val[{}] = {}".format(
                    i, v
                )
            )


class Weight:
    def value(self, sn: SerialNum) -> float:
        pass

    def set_value(self, sn: SerialNum, value: float):
        pass


class EdgeWeight:
    def value(self, edge: Edge) -> float:
        pass

    def set_value(self, edge: Edge, value: float):
        pass


class Lattice:
    def __init__(self, *shape) -> None:
        all_positive(*shape)

    def neighbours(self, sn: SerialNum) -> tuple[SerialNum]:
        pass

    # Point has type
    def __contains__(self, sn: SerialNum) -> bool:
        pass

    def all_serial_num(self) -> tuple[SerialNum]:
        pass

    def to_coord(self, sn: SerialNum) -> tuple[float]:
        pass


class SerialNum:
    __val = None

    def __init__(self, *val) -> None:
        all_positive(*val)
        self.__val = val

    def value(self) -> tuple[int]:
        return self.__val

    def __len__(self):
        return len(self.__val)

    def __eq__(self, other: SerialNum):
        return self.__val == other.value()


class Edge:
    __start = None
    __end = None

    def __init__(self, start: SerialNum, end: SerialNum) -> None:
        self.__start = start
        self.__end = end

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def __eq__(self, other: Edge):
        return self.start() == other.start() and self.__end == other.end()
