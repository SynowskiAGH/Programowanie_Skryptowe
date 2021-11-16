from DeanerySystem.day import Day

class Term:
    def __init__(self, hour, minute, duration = 90, day: Day = Day.MON): #Konstruktor
        self.hour = hour
        self.minute = minute
        self.duration = duration
        self._day = day

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

    def __sub__(first, second):
        first_hour = first.duration // 60
        first_minute = first.duration % 60
        first.hour = first.hour + first_hour
        first.minute = first.minute + first_minute
        ret_hour = (first.hour-second.hour)*60
        ret_minute = first.minute-second.minute
        return Term(second.hour, second.minute, (ret_hour+ret_minute))

        


    def __str__(self):
        return(f"{self.hour}:{self.minute} [{self.duration}]")

    def laterThan(self, termin):
        if Day.difference(self._day, termin._day) < 0:
            return True
        if Day.difference(self._day, termin._day) == 0:
            if termin.hour < self.hour:
                return True
            elif termin.hour == self.hour and termin.minute < self.minute:
                return True
            return False
        return False

    def equals (self, termin):
        return True if Day.difference(self._day, termin._day) == 0 and termin.hour == self.hour and termin.minute == self.minute and termin.duration == self.duration else False
    
    def earlierThan(self, termin):
        if Day.difference(self._day, termin._day) > 0:
            return True
        elif Day.difference(self._day, termin._day) == 0:
            if termin.hour > self.hour:
                return True
            elif termin.hour == self.hour and termin.minute > self.minute:
                return True
            return False
        return False

