def add_in_f(n1, n2, modulo):
    return (n1 + n2) % modulo

def multiply_in_f(n1, n2, modulo):
    return (n1 * n2) % modulo

def to_binary(n):
    return bin(int(n))[2:]   # skip '0b'

def square_iterative(basis, exponent, modulo):
### first cover the basic cases    
    if basis == 0:
        return 0
    if basis == 1 or exponent == 0:
        return 1

    exp_bin = to_binary(exponent)
    res = basis

    for b in exp_bin[1:]:
        res = multiply_in_f(res, res, modulo)
        if b == '1':
            res = multiply_in_f(res, basis, modulo)
    
    return res

def is_quadratic_residue(residue, modulo):
    exp = (modulo - 1) / 2
    res = square_iterative(residue, exp, modulo)
    if res == 1:
        return True
    else:
        return False

def get_quadratic_root(residue, modulo):
    if not is_quadratic_residue(residue, modulo) or modulo % 4 != 3:
        return None
    exp = (modulo + 1) / 4
    return square_iterative(residue, exp, modulo)

def get_inverse(n, modulo):
    pass