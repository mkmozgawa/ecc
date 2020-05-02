
import math

class EPoint:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def reverse_y(self):
        return EPoint(self.x, -self.y)
    
    def get_coordinates(self):
        return (self.x, self.y)

    def decode(self, mi):
        num = (self.x-1)//mi
        return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode()
