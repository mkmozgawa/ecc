import math
from random import SystemRandom
from EPoint import EPoint
from helpers import generate_random_number, get_inverse, get_y_2

class ECurve:
    points = [(math.inf, math.inf)]

    def __init__(self, a, b, p):
        if self._is_delta_0(a, b, p) and not math.isinf(a) and not math.isinf(b):
            raise AssertionError('Niepoprawne równanie krzywej. Wyróżnik równy 0.')
        self.__a = a
        self.__b = b
        self.__p = p
        self.__order = self.p + 1 - abs(math.floor(2 * math.sqrt(self.p)))

    @property
    def p(self):
        return self.__p

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def order(self):
        return self.__order

    def _is_delta_0(self, a, b, p): # a, b, p since this happens before the assignment of values in the object
        delta = (4 * a**3 + 27 * b**2) % p
        return delta == 0
    
    def print_equation(self):
        print('E/F_%s: y^2 = x^3 + %sx + %s' % (self.p, self.a, self.b))

    def print_points(self):
        print('E(F_%s): ' % self.p + str([v for v in self.points]))

    def append_point(self, point):
        if not self.is_point_on_ec(point):
            raise AssertionError('Podany punkt nie leży na zadanej krzywej.')
        self.points.append((point.x,point.y))

    def generate_random_point(self):
        res = -1
        while res != 1:
            x = generate_random_number(self.p)
            y_2 = get_y_2(x, self.a, self.b, self.p)
            res = pow(y_2, (self.p - 1) // 2, self.p)
        y = pow(y_2, (self.p + 1) // 4, self.p)
        return EPoint(x, y)

    def is_point_on_ec(self, point):
        return (pow(point.x, 3, self.p) + self.a * point.x + self.b) % self.p == (pow(point.y, 2, self.p)) % self.p

    def double_point(self, point):
        lam = ((3*pow(point.x, 2, self.p) + self.a) * get_inverse(2*point.y, self.p)) % self.p
        x3 = (pow(lam, 2, self.p) - 2*point.x) % self.p
        y3 = (lam*(point.x-x3) - point.y) % self.p
        return EPoint(x3, y3)

    def multiply_point_binary(self, point, n):
        n_bin_k_2 = bin(n)[3:]
        Q = point
        for e in n_bin_k_2:
            Q = self.add_points(Q, Q)
            if e == '1':
                Q = self.add_points(Q, point)
        return Q

    def add_points(self, point_1, point_2):
        if isinstance(point_1.x, float) and math.isinf(point_1.x):
            return point_2
        if isinstance(point_2.x, float) and math.isinf(point_2.x):
            return point_1
        if ((point_1.y  + point_2.y) % self.p) == 0 and point_1.x == point_2.x:
            return EPoint(math.inf, math.inf)
        if point_1.x == point_2.x and point_1.y == point_2.y:
            return self.double_point(point_1)
        lam = ((point_2.y - point_1.y) * get_inverse(point_2.x - point_1.x, self.p)) % self.p
        x3 = (pow(lam, 2, self.p) - point_1.x - point_2.x) % self.p
        y3 = (lam * (point_1.x - x3) - point_1.y) % self.p
        return EPoint(x3, y3)
