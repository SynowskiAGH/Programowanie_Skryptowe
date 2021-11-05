from day import Day
from term import Term


class Lesson(object):
    def __init__(self, term: Term, name: str, teacherName: str, year: int, full_time: bool = True):
        self.term = term
        self.name = name
        self.teacherName = teacherName
        self.year = year
        self.full_time = full_time

    @property
    def term(self):
        return self._term

    @property
    def name(self):
        return self._name

    @property
    def teacherName(self):
        return self._teacher_name

    @property
    def year(self):
        return self._year

    @property
    def fullTime(self):
        return self._full_time

    @term.setter
    def setTerm(self, term):
        self._term = term

    @name.setter
    def setName(self, name):
        self._name = name

    @teacherName.setter
    def setTeacherName(self, name):
        self._teacher_name = name

    @year.setter
    def setYear(self, year):
        self._year = year

    @fullTime.setter
    def setFullTime(self, full_time):
        self._full_time = full_time

    def earlierDay(self):
        changed_day = Day(7 if self._term._day.value - 1 == 0 else self._term._day.value - 1)
        new_term = Term(self._term._hour, self._term._minute, self._term._duration, changed_day)

    def laterDay(self):
        changed_day = Day(1 if self._term._day.value + 1 == 8 else self._term._day.value + 1)
        new_term = Term(self._term._hour, self._term._minute, self._term._duration, changed_day)

    def earlierTime(self):
        hour_difference = self._term.duration // 60
        minute_difference = self._term.duration % 60

        if self._term.minute - minute_difference < 0:
            minute_difference -= 60 #Cofam się o jedną godzinę
            hour_difference += 1

        self._term.hour -= hour_difference
        self._term.minute -= minute_difference
        return True

    def laterTime(self):
        hour_difference = self._term.duration // 60
        minute_difference = self._term.duration % 60

        if self._term.minute - minute_difference >= 60:
            minute_difference -= 60 #Cofam się o jedną godzinę
            hour_difference += 1

        self._term.hour += hour_difference
        self._term.minute += minute_difference
        return True
    
