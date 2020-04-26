from helpers import generate_random_number

class ElGamalCipher:

    def __init__(self):
        pass

    def encrypt(public_key, message_point):
        y = generate_random_number(public_key.ec.p)
        C_1 = public_key.ec.multiply_point_binary(message_point, y)
        C_2 = public_key.ec.add_points(message_point, 
            public_key.ec.multiply_point_binary(public_key.Q, y))
        return (C_1, C_2)

    def decrypt(private_key, C_1, C_2):
        x_C_1 = private_key.ec.multiply_point_binary(C_1, private_key.x)
        return private_key.ec.add_points(C_2, x_C_1.reverse_y())