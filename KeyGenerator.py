from ECurve import ECurve
from EPoint import EPoint
from Key import Key
from helpers import generate_random_number

class KeyGenerator:

    def __init__(self, ec):
        self.ec = ec
        self.__P = ec.generate_random_point()
        self.__x = generate_random_number(ec.order, start=0)
        self.__Q = ec.multiply_point_binary(self.__P, self.__x)

    @property
    def public_key(self):
        return Key(self.ec, self.__P, self.__Q)

    @property
    def private_key(self):
        return Key(self.ec, self.__P, self.__Q, self.__x)
