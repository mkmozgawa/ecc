
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
    # ec = ECurve(0, 9, 419)
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

    print("1. Alice generuje klucze")
    keys = KeyGenerator(ec)

    print('2. Bob koduje wiadomość "hello"')
    M = Message("twoja stara pierze w rzece")
    M_P, mi = M.encode(ec)
    print('Wiadomość zakodowana w punkcie:')
    print(M_P.get_coordinates())

    print("3. Bob pobiera klucz Alice")
    public_key = keys.public_key

    print("4. Bob szyfruje wiadomość")
    C_1, C_2 = ElGamalCipher.encrypt(public_key, M_P)
    print('C1:')
    print(C_1.get_coordinates())
    print('C2:')
    print(C_2.get_coordinates())

    print("4. Alice deszyfruje wiadomość")
    M_P_D = ElGamalCipher.decrypt(keys.private_key, C_1, C_2)
    print('Zdeszyfrowany punkt:')
    print(M_P_D.get_coordinates())

    print("5. Alice odkodowuje wiadomość")
    print('wiadomość: %s' % M_P_D.decode(mi))