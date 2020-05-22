import unittest
import math

from helpers import get_inverse, generate_random_number, get_hash_sha256_hex, get_hash_sha256_bytes
from EPoint import EPoint
from ECurve import ECurve
from ElGamalCipher import ElGamalCipher
from ElGamalKey import ElGamalKey
from ElGamalKeyGenerator import ElGamalKeyGenerator
from Message import Message
from ECDSA import ECDSA
from ECDSAKeyGenerator import ECDSAKeyGenerator

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

    def test_rng_generates_number_less_than_x(self):
        self.assertLess(generate_random_number(30), 30)
    
    def test_rng_gneerates_number_from_x_inclusive_to_y_exclusive(self):
        n = generate_random_number(100, 30)
        self.assertGreaterEqual(n, 30)
        self.assertLess(n, 100)

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
        self.assertTrue(self.ec.is_point_on_ec(self.ec.add_points(self.p, self.p2)))

    def test_adding_points_that_results_in_infinity_works(self):
        self.assertEqual(self.ec.add_points(self.p, self.p3).get_coordinates(),
        self.p_inf.get_coordinates())

    def test_doubling_a_point_returns_correct_result(self):
        self.assertEqual(self.ec.double_point(self.p).get_coordinates(), ECURVE_POINTS[1])
        self.assertTrue(self.ec.is_point_on_ec(self.ec.double_point(self.p)))

    def test_multiplying_a_point_twice_returns_the_same_result_as_doubling_it(self):
        self.assertEqual(self.ec.multiply_point_binary(self.p, 2).get_coordinates(), 
        self.ec.double_point(self.p).get_coordinates())
        self.assertTrue(self.ec.is_point_on_ec(self.ec.multiply_point_binary(self.p, 2)))

    def test_multiplying_with_infinity_as_result_works(self):
        self.assertEqual(self.ec.multiply_point_binary(self.p, 3).get_coordinates(), (math.inf, math.inf))
        self.assertEqual(self.ec.multiply_point_binary(
            EPoint(ECURVE_POINTS[7][0], ECURVE_POINTS[7][1]), 6).get_coordinates(), 
            (math.inf, math.inf))

    def test_multiplying_a_point_across_infinity_works(self):
        self.assertEqual(self.ec.multiply_point_binary(self.p, 4).get_coordinates(), (0,3))
        self.assertTrue(self.ec.is_point_on_ec(self.ec.multiply_point_binary(self.p, 4)))


class ElGamalKeyGeneratorTestCase(unittest.TestCase):
    
    def setUp(self):
        self.ec = ECurve(ECURVE_A, ECURVE_B, ECURVE_P)
        self.key = ElGamalKeyGenerator(self.ec)

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

    def test_generated_points_lie_on_the_curve(self):
        self.assertTrue(self.ec.is_point_on_ec(self.key.public_key.P))
        self.assertTrue(self.ec.is_point_on_ec(self.key.public_key.Q))

    def test_generated_points_are_the_same_for_private_and_public_key(self):
        self.assertEqual(self.key.public_key.P.x, self.key.private_key.P.x)
        self.assertEqual(self.key.public_key.P.y, self.key.private_key.P.y)


class MessageEncodingDecodingTestCase(unittest.TestCase):

    def setUp(self):
        self.ec = ECurve(-3, 
            int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16),
            2**256 - 2**224 + 2**192 + 2**96 - 1)

    def test_encode_decode_gives_back_the_original_value(self):
        mes = Message("hello world")
        pm, mi = mes.encode(self.ec)
        self.assertEqual(pm.decode(mi), mes.text)


class SHA256HashTestCase(unittest.TestCase):

    def test_sha256_returns_correct_values(self):
        mes = "hello world"
        h = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        h_bytes = bytes.fromhex(h)
        self.assertEqual(h, get_hash_sha256_hex(mes))
        self.assertEqual(h_bytes, get_hash_sha256_bytes(mes))


class ECDSATestCase(unittest.TestCase):

    def setUp(self):
        self.ec = ECurve(-3, 
            int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16),
            2**256 - 2**224 + 2**192 + 2**96 - 1)
        self.P = EPoint(48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109, order=2**256 - 2**224 + 2**192 - 89188191075325690597107910205041859247)

    def test_using_correct_signature_on_correct_message_works(self):
        mes = "hello world"
        M = Message(mes)
        keys_Alice = ECDSAKeyGenerator(self.ec, self.P)
        signature = ECDSA().sign(keys_Alice.private_key, M.hash_hex_int)
        self.assertTrue(ECDSA().verify_sign(keys_Alice.public_key, signature, M.hash_hex_int))
        
    def test_using_incorrect_signature_on_correct_message_raises_assertion_error(self):
        mes = "hello world"
        M = Message(mes)
        keys_Alice = ECDSAKeyGenerator(self.ec, self.P)
        signature = ECDSA().sign(keys_Alice.private_key, M.hash_hex_int)
        keys_Mallory = ECDSAKeyGenerator(self.ec, self.P)
        self.assertRaises(AssertionError, ECDSA().verify_sign, keys_Mallory.public_key, signature, M.hash_hex_int)

    def test_using_correct_signature_on_incorrect_message_raises_assertion_error(self):
        mes = "hello world"
        M = Message(mes)
        keys_Alice = ECDSAKeyGenerator(self.ec, self.P)
        signature = ECDSA().sign(keys_Alice.private_key, M.hash_hex_int)
        mes_wrong = "the eagle flies at midnight"
        M_wrong = Message(mes_wrong)
        self.assertRaises(AssertionError, ECDSA().verify_sign, keys_Alice.public_key, signature, M_wrong.hash_hex_int)

    def test_using_incorrect_signature_on_incorrect_message_raises_assertion_error(self):
        mes = "hello world"
        M = Message(mes)
        keys_Alice = ECDSAKeyGenerator(self.ec, self.P)
        signature = ECDSA().sign(keys_Alice.private_key, M.hash_hex_int)
        mes_wrong = "the eagle flies at midnight"
        M_wrong = Message(mes_wrong)
        keys_Mallory = ECDSAKeyGenerator(self.ec, self.P)
        self.assertRaises(AssertionError, ECDSA().verify_sign, keys_Mallory.public_key, signature, M_wrong.hash_hex_int)


if __name__ == '__main__':
    unittest.main()
