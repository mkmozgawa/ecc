from helpers import generate_random_number, get_inverse
from ECDSAKey import ECDSAKey
from ECDSASignature import ECDSASignature

class ECDSA:

    def __init__(self):
        pass

    def sign(self, private_key, message_hex):
        r = 0
        s = 0
        while s == 0:
            while r == 0:
                k = generate_random_number(private_key.P.order, 1) # 1 to q-1 inc
                kP = private_key.ec.multiply_point_binary(private_key.P, k)
                r = kP.x % private_key.P.order
            w = get_inverse(k, private_key.P.order)
            s = (w * (message_hex + private_key.x * r)) % private_key.P.order
        return ECDSASignature(s, r)

    def verify_sign(self, public_key, signature, message_hex):
        v = get_inverse(signature.s, public_key.P.order)
        u1 = (message_hex * v) % public_key.P.order
        u2 = (signature.r * v) % public_key.P.order
        u1P = public_key.ec.multiply_point_binary(public_key.P, u1)
        u2Q = public_key.ec.multiply_point_binary(public_key.Q, u2)
        X = public_key.ec.add_points(u1P, u2Q)
        if X.is_infinite():
            raise AssertionError('Błędny podpis! X = O')
        z = X.x % public_key.P.order
        if z != signature.r:
            raise AssertionError('Błędny podpis!!!')
        return True
