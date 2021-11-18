from DeanerySystem.term import Term

class Break:
    def __init__(self, term):
        self.__term = term

    def __str__():
        return "Przerwa"

    def getTerm(self):
        return self.term

    @property
    def term(self):
        return self.__term

    @term.setter
    def term(self, value):
        self.__term = value


    

