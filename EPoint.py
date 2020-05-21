
import math

class EPoint:

    def __init__(self, x, y, order=None):
        self.__x = x
        self.__y = y
        self.__order = order

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def order(self):
        return self.__order

    def reverse_y(self):
        return EPoint(self.x, -self.y)
    
    def get_coordinates(self):
        return (self.x, self.y)

    def is_infinite(self):
        return self.x == math.inf

    def decode(self, mi):
        num = (self.x-1)//mi
        return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode()
