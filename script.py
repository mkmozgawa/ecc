
import math

from EPoint import EPoint
from ECurve import ECurve
from Message import Message
from ElGamalKeyGenerator import ElGamalKeyGenerator
from ElGamalCipher import ElGamalCipher
from ECDSAKeyGenerator import ECDSAKeyGenerator
from helpers import generate_random_number, get_inverse

if __name__ == "__main__":
    prime = 2**256 - 2**224 + 2**192 + 2**96 - 1
    A = -3
    B = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
    #p = 235322474717419
    # mi = 0
    # v = 8856682
    # # ec = ECurve(0, 9, 419)
    ec = ECurve(A, B, prime)
    # ec = ECurve(mi, v, p)
    # point = ec.generate_random_point()
    # print(point.get_coordinates())

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

    # print("1. Alice generuje klucze")
    # keys = ElGamalKeyGenerator(ec)

    # print('2. Bob koduje wiadomość "hello"')
    # M = Message("twoja stara pierze w rzece")
    # M_P, mi = M.encode(ec)
    # print('Wiadomość zakodowana w punkcie:')
    # print(M_P.get_coordinates())

    # print("3. Bob pobiera klucz Alice")
    # public_key = keys.public_key

    # print("4. Bob szyfruje wiadomość")
    # C_1, C_2 = ElGamalCipher.encrypt(public_key, M_P)
    # print('C1:')
    # print(C_1.get_coordinates())
    # print('C2:')
    # print(C_2.get_coordinates())

    # print("4. Alice deszyfruje wiadomość")
    # M_P_D = ElGamalCipher.decrypt(keys.private_key, C_1, C_2)
    # print('Zdeszyfrowany punkt:')
    # print(M_P_D.get_coordinates())

    # print("5. Alice odkodowuje wiadomość")
    # print('wiadomość: %s' % M_P_D.decode(mi))

    ### ECDSA
    print("1. Alice generuje klucze")
    q = 2**256 - 2**224 + 2**192 - 89188191075325690597107910205041859247
    P = EPoint(48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109, order=q)
    assert ec.append_point(P), "Podany punkt nie leży na tej krzywej"
    keys = ECDSAKeyGenerator(ec, P)

    print('2. Alice generuje podpis do wiadomości M')
    r = 0
    s = 0
    while s == 0:
        while r == 0:
            k = generate_random_number(q, 1) # 1 to q-1 inc
            kP = ec.multiply_point_binary(P, k)
            r = kP.x % q
        w = get_inverse(k, q)
        h = int(Message("the eagle lands at midnight").hash_hex, 16)
        s = (w * (h + keys.private_key.x*r)) % q
    sigAlice = (s, r)

    print('3. Bob weryfikuje podpis')
    h2 = int(Message("the eagle lands at midnight").hash_hex, 16)
    v = get_inverse(s, q)
    u1 = (h2 * v) % q
    u2 = (r * v) % q
    u1P = ec.multiply_point_binary(P, u1)
    u2Q = ec.multiply_point_binary(keys.private_key.Q, u2)
    X = ec.add_points(u1P, u2Q)
    if X.is_infinite():
        raise AssertionError('Błędny podpis!!! X = O')
    z = X.x % q
    if z != r:
        raise AssertionError('Błędny podpis!!!')
    print('Weryfikacja udana')