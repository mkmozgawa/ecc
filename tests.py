import unittest
import math

from helpers import get_inverse
from EPoint import EPoint
from ECurve import ECurve
from ElGamalCipher import ElGamalCipher
from Key import Key
from KeyGenerator import KeyGenerator
from Message import Message

POINT_X = 0
POINT_Y = 1
ECURVE_A = 0
ECURVE_B = 9
ECURVE_P = 11
ECURVE_POINTS = [(0,3), (0,8), (3,5), (3,6), (6,4), (6,7), (7,0), (8,2), (8,9), 
  (9,1), (9,10), (math.inf, math.inf)]

class HelpersTestCase(unittest.TestCase):
    def test_inverse_of_number_returns_correct_result(self):
        self.assertEqual(get_inverse(3,7), 5)

    def test_inverse_of_zero_returns_infinity(self):
        self.assertEqual(get_inverse(0, 11), math.inf)

class EPointTestCase(unittest.TestCase):
    def setUp(self):
        self.point = EPoint(POINT_X, POINT_Y)

    def test_point_initiated_with_correct_values(self):
        self.assertEqual(self.point.x, POINT_X)
        self.assertEqual(self.point.y, POINT_Y)

    def test_point_initiated_with_infinity_values(self):
        inf_point = EPoint(math.inf, math.inf)
        self.assertTrue(math.isinf(inf_point.x))
        self.assertTrue(math.isinf(inf_point.y))

    def test_get_point_coordinates_returns_a_tuple(self):
        self.assertEqual(self.point.get_coordinates(), (POINT_X, POINT_Y))

    def test_reversing_a_point_returns_x_minus_y(self):
        rev_point = self.point.reverse_y()
        self.assertEqual(rev_point.x, self.point.x)
        self.assertEqual(rev_point.y, -self.point.y)

class ECurveTestCase(unittest.TestCase):
    def setUp(self):
        self.ec = ECurve(ECURVE_A, ECURVE_B, ECURVE_P)
        self.p = EPoint(ECURVE_POINTS[0][0], ECURVE_POINTS[0][1])
        self.p2 = EPoint(ECURVE_POINTS[2][0], ECURVE_POINTS[2][1])
        self.p3 = EPoint(ECURVE_POINTS[1][0], ECURVE_POINTS[1][1])
        self.p_inf = EPoint(ECURVE_POINTS[-1][0], ECURVE_POINTS[-1][0])

    def test_generate_random_point_finds_a_point_on_ec(self):
        self.assertIn(self.ec.generate_random_point().get_coordinates(), 
        ECURVE_POINTS)

    def test_adding_point_to_infinity_returns_that_point(self):
        self.assertEqual(self.ec.add_points(self.p, self.p_inf).get_coordinates(), 
        ECURVE_POINTS[0])
    
    def test_adding_point_to_itself_returns_multiplication(self):
        self.assertEqual(self.ec.add_points(self.p, self.p).get_coordinates(), 
        self.ec.double_point(self.p).get_coordinates())
    
    def test_adding_point_to_another_returns_correct_result(self):
        self.assertEqual(self.ec.add_points(self.p, self.p2).get_coordinates(),
        (6,4))

    def test_adding_points_that_results_in_infinity_works(self):
        self.assertEqual(self.ec.add_points(self.p, self.p3).get_coordinates(),
        self.p_inf.get_coordinates())

    def test_doubling_a_point_returns_correct_result(self):
        self.assertEqual(self.ec.double_point(self.p).get_coordinates(), ECURVE_POINTS[1])

    def test_multiplying_a_point_twice_returns_the_same_result_as_doubling_it(self):
        self.assertEqual(self.ec.multiply_point_binary(self.p, 2).get_coordinates(), 
        self.ec.double_point(self.p).get_coordinates())

    def test_multiplying_with_infinity_as_result_works(self):
        self.assertEqual(self.ec.multiply_point_binary(self.p, 3).get_coordinates(), (math.inf, math.inf))
        self.assertEqual(self.ec.multiply_point_binary(
            EPoint(ECURVE_POINTS[7][0], ECURVE_POINTS[7][1]), 6).get_coordinates(), 
            (math.inf, math.inf))

    def test_multiplying_a_point_across_infinity_works(self):
        self.assertEqual(self.ec.multiply_point_binary(self.p, 4).get_coordinates(), (0,3))

class KeyGeneratorTestCase(unittest.TestCase):
    
    def setUp(self):
        self.ec = ECurve(ECURVE_A, ECURVE_B, ECURVE_P)
        self.key = KeyGenerator(self.ec)

    def test_public_key_contains_ec_and_two_points(self):
        self.assertIsInstance(self.key.public_key.ec, ECurve)
        self.assertIsInstance(self.key.public_key.P, EPoint)
        self.assertIsInstance(self.key.public_key.Q, EPoint)
        self.assertIsNone(self.key.public_key.x)

    def test_private_key_contains_ec_and_two_points_and_x(self):
        self.assertIsInstance(self.key.private_key.ec, ECurve)
        self.assertIsInstance(self.key.private_key.P, EPoint)
        self.assertIsInstance(self.key.private_key.Q, EPoint)
        self.assertIsNotNone(self.key.private_key.x)

# class ElGamalCipherTestCase(unittest.TestCase):

#     def setUp(self):
#         self.ec = ECurve(ECURVE_A, ECURVE_B, ECURVE_P)
#         self.p = ECURVE_POINTS[0]
#         self.elcipher = ElGamalCipher()

#     def test_encryption_returns_two_points(self):
#         self.assertTrue(len(self.elcipher.encrypt()))

class MessageEncodingDecodingTestCase(unittest.TestCase):

    def setUp(self):
        self.ec = ECurve(-3, 
            int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16),
            2**256 - 2**224 + 2**192 + 2**96 - 1)

    def test_encode_decode_gives_back_the_original_value(self):
        mes = Message("hello world")
        print(mes.number)
        pm, mi = mes.encode(self.ec)
        self.assertEqual(pm.decode(mi), mes.text)

if __name__ == '__main__':
    unittest.main()
