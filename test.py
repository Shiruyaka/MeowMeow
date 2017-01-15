class Ala:
    def __init__(self):
        print('a')

class Bob(Ala):
    def __init__(self, var):
        Ala.__init__(self)
        self.var = var
        print('b')

class Cecylia(Bob):
    def __init__(self, vara, var2):
        Bob.__init__(self, vara)
        self.var = var2
        print('c')


c = Cecylia(3, 5)