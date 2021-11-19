from DeanerySystem.day import Day
from DeanerySystem.term import Term
from DeanerySystem.teacher import Teacher

class Lesson():
    def __init__(self, timetable, term, name, teacherName, year):
        self.__timetable = timetable
        self.__term = term
        self.__name = name
        self.__teacherName = teacherName
        self.__teacher = None
        self.__year = year
        self.__full_time = self.term_check()

    def term_check(self):
        if self.__term.day.value < 5:
            return True
        elif self.__term.day.value > 5:
            return False
        
        if self.__term.hour < 17:
            return True
        else:
            return False

    @property
    def teacher(self):
        return self.__teacher
        
    @property
    def timetable(self):
        return self.__timetable

    @property
    def term(self):
        return self.__term

    @property
    def name(self):
        return self.__name

    @property
    def teacherName(self):
        return self.__teacherName

    @property
    def year(self):
        return self.__year

    @property
    def full_time(self):
        return self.__full_time

    @teacher.setter
    def teacher(self, value):
        self.__teacher = value

    @timetable.setter
    def timetable(self, value):
        self.__timetable = value

    @term.setter
    def term(self, value):
        if type(value) is not Term:
            raise TypeError('term musi być typu \'Term\'')
        else:
            self.__term = value

    @name.setter
    def name(self, value):
        if type(value) is not str:
            raise TypeError('name musi być typu \'str\'')
        else:
            self.__term = value

    @teacherName.setter
    def teacherName(self, value):
        if type(value) is not str:
            raise TypeError('teacherName musi być typu \'str\'')
        else:
            self.__teacherName = value
    
    @year.setter
    def year(self, value):
        if type(value) is not int:
            raise TypeError('rok musi być liczbą całkowitą')
        elif value <= 0:
            raise ValueError('rok musi być liczbą dodatnią')
        else:
            self.__year = value

    def __str__(self):
        if self.__year == 1:
            year_str = 'Pierwszy rok'

        elif self.__year == 2:
            year_str = 'Drugi rok'

        elif self.__year == 3:
            year_str = 'Trzeci rok'

        elif self.__year == 4:
            year_str = 'Czwarty rok'

        elif self.__year == 5:
            year_str = 'Piąty rok'

        if self.__full_time:
            time_str = 'stacjonarnych'
        else:
            time_str = 'niestacjonarnych'

        return (f'{self.__name} ({self.__term.day} {self.__term.printStartTime()}-{self.__term.printEndTime()})\n'
                f'{year_str} studiów {time_str}\n'
                f'Prowadzący: {self.__teacherName}')

    def __add__(self, value):
        if type(value) is Teacher:
            new_time = value.time + self.__term.duration
            if new_time <= 270:
                value.time = new_time
                self.__teacher = None #Usuwanie teachera
                self.__teacher = value #Nadpisywanie teachera
        return self.__teacher

    def __sub__(self, value):
        if type(value) is Teacher:
            new_time = value.time - self.__term.duration
            value.time = new_time
            self.__teacher = None
        return self.__teacher



    def earlierDay(self):
        new_day_value = self.__term.day.value - 1

        if new_day_value < 1:
            return False

        new_day = Day(new_day_value)
        nt = Term(self.__term.hour, self.__term.minute, new_day)

        if not self.timetable.can_be_transferred_to(nt, self.full_time):
            return False

        self.__term.day = new_day 
        return True

    def laterDay(self):
        new_day_value = self.__term.day.value + 1

        if new_day_value > 7:
            return False

        new_day = Day(new_day_value)
        new_term = Term(self.__term.hour, self.__term.minute, new_day)

        if not self.timetable.can_be_transferred_to(new_term, self.full_time):
            return False

        self.__term.day = new_day
        return True

    def earlierTime(self):
        hour_diff = self.__term.duration // 60
        min_diff = self.__term.duration % 60

        if self.__term.minute - min_diff < 0:
            min_diff -= 60
            hour_diff += 1

        new_term = Term(self.__term.hour - hour_diff, self.__term.minute - min_diff, self.__term.day)

        if hasattr(self.timetable, 'breaks'):
            if not self.timetable.skipBreaks: #skipbreaks = false
                overlaps_bool = self.timetable.overlapsBreak(new_term) #Sprawdzam, czy najeżdżam na przerwy

                if overlaps_bool: #Jeśli najeżdżam, to zwracam false
                    return False
            else:
                overlaps_bool = self.timetable.overlapsBreak(new_term) #Skipbreaks = true

                if overlaps_bool:

                    hour_diff += overlaps_bool[1] // 60 #mechanizm przenoszenia przez przerwę
                    min_diff += overlaps_bool[1] % 60

                    if self.__term.minute - min_diff < 0:
                        min_diff -= 60
                        hour_diff += 1

                    new_term = Term(self.__term.hour - hour_diff, self.__term.minute - min_diff, self.__term.day)

        if not self.timetable.can_be_transferred_to(new_term, self.full_time):
            return False

        self.__term.hour -= hour_diff
        self.__term.minute -= min_diff
        return True


    def laterTime(self):
        hour_diff = self.__term.duration // 60
        min_diff = self.__term.duration % 60

        if self.__term.minute + min_diff >= 60:
            min_diff -= 60
            hour_diff += 1

        new_term = Term(self.__term.hour + hour_diff, self.__term.minute + min_diff, self.__term.day)

        if hasattr(self.timetable, 'breaks'):
            if not self.timetable.skipBreaks: #skipbreaks = false
                overlaps_bool = self.timetable.overlapsBreak(new_term)  #Sprawdzam, czy najeżdżam na przerwy
                
                if overlaps_bool: #Jeśli najeżdżam, to zwracam false
                    return False

            else:
                overlaps_bool = self.timetable.overlapsBreak(new_term) #Skipbreaks = true
                
                if overlaps_bool:
                    hour_diff += overlaps_bool[1] // 60 #mechanizm przenoszenia przez przerwę
                    min_diff += overlaps_bool[1] % 60

                    if self.__term.minute - min_diff < 0:
                        min_diff -= 60
                        hour_diff += 1

                    new_term = Term(self.__term.hour - hour_diff, self.__term.minute - min_diff, self.__term.day)

        if not self.timetable.can_be_transferred_to(new_term, self.full_time):
            return False

        self.__term.hour += hour_diff
        self.__term.minute += min_diff
        return True
