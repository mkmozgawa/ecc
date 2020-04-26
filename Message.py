

import binascii

from helpers import generate_random_number, get_y_2, get_legendre_symbol_value, get_root_from_legendre
from EPoint import EPoint

class Message:

    def __init__(self, message_ascii):
        self.__text = message_ascii
        self.__number = int(bin(int.from_bytes(message_ascii.encode(), 'big')), 2)

    @property
    def text(self):
        return self.__text

    @property
    def number(self):
        return self.__number

    def encode(self, ec):
        mi = generate_random_number(50, start=30)
        N = generate_random_number(ec.p//mi, start=self.number)

        for j in list(range(1, mi+1)):
            x = (self.number * mi + j) % ec.p
            y_2 = get_y_2(x, ec.a, ec.b, ec.p)
            if get_legendre_symbol_value(y_2, ec.p) == 1:
                y = get_root_from_legendre(y_2, ec.p)
                if ec.is_point_on_ec(EPoint(x,y)):
                    return (EPoint(x,y), mi)
