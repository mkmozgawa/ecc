import unittest
from utils import add_in_f, multiply_in_f, to_binary, square_iterative, is_quadratic_residue, get_quadratic_root

class AddInFTestCase(unittest.TestCase):

    def test_adds_two_simple_numbers(self):
        self.assertEqual(add_in_f(1, 1, 11), 2)

    def test_adds_two_numbers_with_overlap(self):
        self.assertEqual(add_in_f(5, 8, 11), 2)

    def test_adds_negative_number(self):
        self.assertEqual(add_in_f(-5, 4, 11), 10)
    
    def test_adds_two_negative_numbers(self):
        self.assertEqual(add_in_f(-5, -5, 11), 1)

class MultiplyInFTestCase(unittest.TestCase):

    def test_multiplies_two_simple_numbers(self):
        self.assertEqual(multiply_in_f(2, 2, 11), 4)

    def test_multiplies_two_numbers_with_overlap(self):
        self.assertEqual(multiply_in_f(5, 4, 11), 9)

    def test_multiplies_negative_number(self):
        self.assertEqual(multiply_in_f(5, -2, 11), 1)

    def test_multiplies_two_negative_numbers(self):
        self.assertEqual(multiply_in_f(-5, -5, 11), 3)

class ToBinaryTestCase(unittest.TestCase):

    def test_converts_to_binary_string(self):
        self.assertEqual(to_binary(11), '1011')
        self.assertEqual(to_binary(1), '1')
        self.assertEqual(to_binary(0), '0')

class SquareIterative(unittest.TestCase):

    def test_gets_square_iterative(self):
        self.assertEqual(square_iterative(3, 10, 17), 8)
        self.assertEqual(square_iterative(-2, 7, 17), 8)

class QuadraticResidue(unittest.TestCase):

    def test_is_quadratic_residue(self):
        is_qres = [1, 3, 4, 9, 10, 12]
        is_not_qres = list(filter(lambda x: x not in is_qres, list(range(0, 13))))
        for num in is_qres:
            self.assertTrue(is_quadratic_residue(num, 13))
        for num in is_not_qres:
            self.assertFalse(is_quadratic_residue(num, 13))

class QuadraticRoot(unittest.TestCase):

    def test_gets_quadratic_root_if_possible(self):
        self.assertEqual(get_quadratic_root(5, 19), 9)

    def test_returns_None_if_no_quadratic_root_possible(self):
        self.assertIsNone(get_quadratic_root(5, 13))

if __name__ == '__main__':
    unittest.main()