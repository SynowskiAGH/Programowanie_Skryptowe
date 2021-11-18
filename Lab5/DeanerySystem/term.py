from DeanerySystem.day import Day
from DeanerySystem.basicterm import BasicTerm

class Term(BasicTerm):
    def __init__(self, hour, minute, day: Day = Day.MON,  duration: int = 90): #Konstruktor
        super().__init__(hour, minute, duration)
        self.__day = day

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, value):
        if type(value) is not Day:
            raise TypeError('Dzień musi być typu \'Day\'')
        else:
            self.__day = value

    def __lt__(self, other):
        return Term.earlierThan(self, other)

    def __le__(self, other):
        return Term.earlierThan(self, other) or Term.equals(self, other)

    def __eq__(self, other):
        return Term.equals(self, other)

    def __ge__(self, other):
        return Term.laterThan(self, other) or Term.equals(self, other)

    def __gt__(self, other):
        return Term.laterThan(self, other) 

    def __str__(self):
        return(f"{self.hour}:{self.minute} [{self.duration}]")

    def laterThan(self, Termin):
        if Day.difference(self.__day, Termin.day) < 0:
            return True
        if Day.difference(self.__day, Termin.day) == 0:
            if Termin.hour < self.hour:
                return True
            elif Termin.hour == self.hour and Termin.minute < self.minute:
                return True
            return False
        return False

    def equals (self, Termin):
        return True if Day.difference(self.__day, Termin.day) == 0 and Termin.hour == self.hour and Termin.minute == self.minute and Termin.duration == self.duration else False
    
    def earlierThan(self, Termin):
        if Day.difference(self.__day, Termin.day) > 0:
            return True
        elif Day.difference(self.__day, Termin.day) == 0:
            if Termin.hour > self.hour:
                return True
            elif Termin.hour == self.hour and Termin.minute > self.minute:
                return True
            return False
        return False
