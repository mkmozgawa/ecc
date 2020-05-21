from random import SystemRandom
import math
import hashlib

def generate_random_number(stop, start=None):
    crypto_gen = SystemRandom()
    if start is not None:
        return crypto_gen.randint(start, stop-1)
    return crypto_gen.randrange(stop)

def get_inverse(n, p):
    if n == 0:
        return math.inf
    return pow(n, p-2, p)

def get_y_2(x, a, b, p):
    return ((x ** 3 + a * x + b) % p)

def get_legendre_symbol_value(y_2, p):
    return pow(y_2, (p - 1) // 2, p)

def get_root_from_legendre(y_2, p):
    return pow(y_2, (p + 1) // 4, p)

def get_hash_sha256_hex(message):
    m = hashlib.sha256()
    m.update(str.encode(message))
    return m.hexdigest()

def get_hash_sha256_bytes(message):
    m = hashlib.sha256()
    m.update(str.encode(message))
    return m.digest()