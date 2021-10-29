class Term():
    def __init__(self, day, hour, minute):
        self._day = day
        self.hour = hour
        self.minute = minute
        self.duration = 90

    def __str__(self):
        rep_day = { 1: "Poniedziałek",
                    2: "Wtorek",
                    3: "Środa",
                    4: "Czwartek",
                    5: "Piątek",
                    6: "Sobota",
                    7: "Niedziela",
        }[self._day.value]
        return "{} {}:{} [{}]".format(rep_day, self.hour, self.minute, self.duration)

    def earlierThan(self, termin):
        if termin.hour < self.hour:
            return False
        elif termin.hour == self.hour:
            if termin.minute < self.minute:
                return False
        else:
            return True

    def laterThan(self, termin):
        if termin.hour > self.hour:
            return False
        elif termin.hour == self.hour:
            if termin.minute > self.minute:
                return False
        else:
            return True

    def equals(self, termin):
        return True if self._day.difference(termin._day) == 0 and self.hour == termin.hour and self.minute == termin.minute else False  
