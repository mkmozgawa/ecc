
class ECDSASignature:

    def __init__(self, s, r):
        self.__s = s
        self.__r = r

    @property
    def s(self):
        return self.__s

    @property
    def r(self):
        return self.__r
