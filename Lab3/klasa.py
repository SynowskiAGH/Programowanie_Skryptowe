class Klasa(object):
    tab = [1,2,3]

    def __init__(self, tab, a=0, b=0):
        print("Wywołano metodę '__init__()'")
        self.tab = tab 
        self._zmienna1 = a
        self.__zmienna2 = b

    def __del__(self):
        print("Wywołano metodę '__del__()'")

    def __str__(self):
        print(self.__zmienna2)
        return "Wywołano metodę '__str__()'"

    def __repr__(self):
        return "Wywołano metodę '__repr__()'"

    def metodaInstancyjna(self):
        print("Wywołano metodę 'metodaInstancyjna()'")
        print(self.__class__.tab)

    @classmethod
    def metodaKlasowa(cls):
        print("Wywołano metodę 'metodaKlasowa()'")

    @staticmethod
    def metodaStatyczna():
        print("Wywołano metodę 'metodaStatyczna()'")

        #print(obiekt._Klasa__zmienna2)
