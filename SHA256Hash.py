import hashlib

class SHA256Hash:

    def __init__(self, message):
        self.__hash = hashlib.sha256().update(str.encode(message))
        print(self.__hash)

    @property
    def hash_hex(self):
        return self.__hash.hexdigest()

    @property
    def hash_bytes(self):
        return self.__hash.digest()
