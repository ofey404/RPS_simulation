def all_positive(*val):
    for i, v in enumerate(val):
        if v < 0:
            raise Exception(
                "all fields of serial number should be positive, val[{}] = {}".format(
                    i, v
                )
            )


class SerialNum:
    __val = None

    def __init__(self, *val) -> None:
        all_positive(*val)
        self.__val = val

    def value(self) -> tuple[int]:
        return self.__val

    def __len__(self):
        return len(self.__val)

    def __eq__(self, other):
        return self.__val == other.value()


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


class Weight:
    def value(self, sn: SerialNum) -> float:
        pass


class SideWeight:
    def value(lhs: SerialNum, rhs: SerialNum) -> float:
        pass
