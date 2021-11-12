from DeanerySystem.day import Day

class Term:
    def __init__(self, day, hour, minute): #Konstruktor
        self.hour = hour
        self.minute = minute
        self.duration = 90
        self._day = day


    def __str__(self):
        return(f"{repr(self._day)} {self.hour}:{self.minute} [{self.duration}]")

    def earlierThan(self, termin):
        if Day.difference(self._day, termin._day) < 0:
            return True
        elif Day.difference(self._day, termin._day) == 0:
            if termin.hour < self.hour:
                return True
            if termin.hour == self.hour and termin.minute < self.hour:
                return True
        else: return False

    def equals (self, termin):
        return True if Day.difference(self._day, termin._day) == 0 and termin.hour == self.hour and termin.minute == self.minute else False
    
    def laterThan(self, termin):
        if Day.difference(self._day, termin._day) > 0:
            return True
        elif Day.difference(self._day, termin._day) == 0:
            if termin.hour > self.hour:
                return True
            if termin.hour == self.hour and termin.minute > self.hour:
                return 
        else: False

term1 = Term(Day.TUE, 9, 45)
print(term1)
term2 = Term(Day.WED, 10, 15)
print(term2)
print(term1.earlierThan(term2)) #Ma byc true
print(term1.laterThan(term2)) #Ma byc false
print(term1.equals(term2)) #Ma byc false
