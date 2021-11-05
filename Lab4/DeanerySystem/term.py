from day import Day


class Term(object):
    def __init__(self, hour, minute, duration = 90, day = Day.MON):
        self._hour = hour
        self._minute = minute 
        self._duration = duration
        self._day = day

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def duration(self):
        return self._duration

    @property
    def day(self):
        return self._day
        
    @hour.setter
    def setHour(self, hour):
        self._hour = hour

    @minute.setter
    def setMinute(self, minute):
        self._minute = minute

    @duration.setter
    def setDuration(self, duration):
        self._duration = duration

    @day.setter
    def setDay(self, day):
        self._day = day

    def __str__(self):
        [self._day.value]
        return "{}:{} [{}]".format(self._hour, "0"+str(self._minute) if self._minute >= 0 and self._minute <= 9 else self._minute, self._duration)

    def earlierThan(self, termin):
        return False if termin._hour < self._hour else (False if termin._hour == self._hour and termin._minute < self._minute else True) 

    def equals(self, termin):
        return True if self._day == termin._day and self._hour == termin._hour and self._minute == termin._minute and self._duration == termin._duration else False
    
    def __lt__(self, termin):
        return self.earlierThan(termin)

    def __le__(self, termin):
        return self.earlierThan(termin) or self.equals(termin)

    def __gt__(self, termin):
        return not self.earlierThan(termin)

    def __ge__(self, termin):
        return not self.earlierThan(termin) or self.equals(termin)

    def __eq__(self, termin):
        return self.equals(termin)

    def __sub__(self, termin):
        hour_d  = self._hour + (self._duration // 60) - termin._hour
        min_d   = self._minute + self._duration % 60 - termin._minute 
        new_dur = hour_d*60 + min_d
        return Term(termin.hour, termin.minute, new_dur, termin.day)
