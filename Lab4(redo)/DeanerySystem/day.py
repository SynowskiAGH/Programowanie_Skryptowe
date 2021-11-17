from enum import Enum

class Day(Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7

    def __str__(self):
        str_val = {
            1: 'Poniedziałek',
            2: 'Wtorek',
            3: 'Środa',
            4: 'Czwartek',
            5: 'Piątek',
            6: 'Sobota',
            7: 'Niedziela'
        }
        return str_val[self.value]


    def __repr__(self):
        str_val = {
            1: 'Poniedziałek',
            2: 'Wtorek',
            3: 'Środa',
            4: 'Czwartek',
            5: 'Piątek',
            6: 'Sobota',
            7: 'Niedziela'
        }
        return str_val[self.value]

    def difference(self, day):
        diff = day.value - self.value 
        return (diff-7) if diff>3 else diff if -4<diff<4 else (diff+7)

def nthDayFrom(n, day):
    new__day = day.value + n
    return Day(new__day+7) if new__day<1 else Day(new__day-7) if new__day>7 else Day(new__day)
