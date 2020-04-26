
import math

from EPoint import EPoint
from ECurve import ECurve
from Message import Message
from KeyGenerator import KeyGenerator
from ElGamalCipher import ElGamalCipher


if __name__ == "__main__":
    prime = 2**256 - 2**224 + 2**192 + 2**96 - 1
    A = -3
    B = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
    # ec = ECurve(0, 9, 11)
    ec = ECurve(A, B, prime)

    # print('Punkty: ')
    # p = ec.generate_random_point()
    # print(p.get_coordinates())
    # q = ec.generate_random_point()
    # print(q.get_coordinates())

    # print('P + Q: ')
    # r = ec.add_points(p,q)
    # print(r.get_coordinates())

    # print('2P: ')
    # p2 = ec.add_points(p,p)
    # print(p2.get_coordinates())

    # print('P-P: ')
    # prev = p.reverse_y()
    # pp = ec.add_points(p, prev)
    # print(pp.get_coordinates())

    # print('P+Inf: ')
    # inf = EPoint(math.inf, math.inf)
    # pinf = ec.add_points(p, inf)
    # print(pinf.get_coordinates())

    # print('Sprawdzanie punktu: ')
    # print('Punkt leży na zadanej krzywej' if ec.is_point_on_ec(p) else 'Punkt nie leży na zadanej krzywej')

    print("Alice generuje klucze")
    keys = KeyGenerator(ec)

    print('Bob koduje wiadomość "hello"')
    M = Message("hello")
    M_P, mi = M.encode(ec)
    print('M_P:')
    print(M_P.get_coordinates())

    print("Bob pobiera klucz Alice")
    public_key = keys.public_key

    print("Bob szyfruje wiadomość")
    C_1, C_2 = ElGamalCipher.encrypt(public_key, M_P)
    print(C_1.get_coordinates())
    print(C_2.get_coordinates())

    print("Alice deszyfruje wiadomość")
    M_P_D = ElGamalCipher.decrypt(keys.private_key, C_1, C_2)
    print('M_P_D:')
    print(M_P_D.get_coordinates())

    print("Alice odkodowuje wiadomość")
    # print(mi)
    print(M_P_D.decode(mi))