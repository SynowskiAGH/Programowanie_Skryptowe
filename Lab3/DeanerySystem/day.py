from enum import Enum


class Day(Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7
    def difference(self, day):
        d = day.value - self.value
        if d > 3:
            return d - 7 #Biorę od "drugiej strony"
        elif d < -3:
            return d + 7
        else:
            return d

def nthDayFrom(n, day):
    val = day.value + n
    if val <= 0:
        return Day(val + 7) #Przesuwam tydzień na dodatnie
    else:
        if val >= 8:
            return (Day(val - 7)) 
        else:
            return Day(val)
