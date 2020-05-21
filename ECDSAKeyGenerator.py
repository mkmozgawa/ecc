from ECurve import ECurve
from EPoint import EPoint
from ECDSAKey import ECDSAKey
from helpers import generate_random_number

class ECDSAKeyGenerator:

    def __init__(self, ec, P):
        self.__ec = ec
        self.__P = P
        self.__x = generate_random_number(P.order, start=1) # 1 to q-1 inclusive
        self.__Q = ec.multiply_point_binary(P, self.__x)

    @property
    def public_key(self):
        return ECDSAKey(self.__ec, self.__P, self.__Q)

    @property
    def private_key(self):
        return ECDSAKey(self.__ec, self.__P, self.__Q, self.__x)