class Klasa(object):
	
    def __init__(self, tab, zmienna1, zmienna2):
        print("Wywołano metodę '__init__()'")
        self.tab = [tab]
        self._zmienna1 = zmienna1
        self.__zmienna2 = zmienna2 #print(obiekt._Klasa__zmienna2)


    def __del__(self):
        print("Wywołano metodę '__del__()'")
   
    def __str__(self):
        return "Wywołano metodę '__str__()'"
    
    def __repr__(self):
        return "Wywołano metodę '__repr__()'"
        
    def metodaInstancyjna(self):
        print("Wywołano metodę 'metodaInstancyjna()'")	
        print(Klasa.tab) #Zmienna klasowa (jedna dla całej klasy)
        print(self.tab)  #Zmienna instancyjna (unikalna dla obiektu)
            
    @classmethod
    def metodaKlasowa(cls):
        print("Wywołano metodę 'metodaKlasowa()'")
            
    @staticmethod
    def metodaStatyczna():
        print("Wywołano metodę 'metodaStatyczna()'")