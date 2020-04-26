
class Key:

    def __init__(self, ec, P, Q, x=None):
        self.__ec = ec
        self.__P = P
        self.__Q = Q
        self.__x = x

    @property
    def ec(self):
        return(self.__ec)
    
    @property
    def P(self):
        return(self.__P)

    @property
    def Q(self):
        return(self.__Q)

    @property
    def x(self):
        return self.__x
