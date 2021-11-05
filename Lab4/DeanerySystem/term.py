from day import Day


class Term(object):
    def __init__(self, hour, minute, duration = 90, day = Day.MON):
        self.__hour = hour
        self.__minute = minute 
        self.__duration = duration
        self.__day = day

    @property
    def hour(self):
        return self.__hour

    @property
    def minute(self):
        return self.__minute

    @property
    def duration(self):
        return self.__duration

    @property
    def day(self):
        return self.__day
        
    @hour.setter
    def setHour(self, hour):
        self.__hour = hour

    @minute.setter
    def setMinute(self, minute):
        self.__minute = minute

    @duration.setter
    def setDuration(self, duration):
        self.__duration = duration

    @day.setter
    def setDay(self, day):
        self.__day = day

    def __str__(self):
        [self.__day.value]
        return "{}:{} [{}]".format(self.__hour, "0"+str(self.__minute) if self.__minute >= 0 and self.__minute <= 9 else self.__minute, self.__duration)

    def earlierThan(self, termin):
        if termin.hour < self.__hour:
            return False
        elif termin.hour == self.__hour:
            if termin.minute < self.__minute:
                return False
        else:
            return True

    def laterThan(self, termin):
        if termin.hour > self.__hour:
            return False
        elif termin.hour == self.__hour:
            if termin.minute > self.__minute:
                return False
        else:
            return True

    def equals(self, termin):
        return True if self.__day.difference(termin.day) == 0 and self.__hour == termin.hour and self.__minute == termin.minute else False 
    
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
        add_hour = self.__duration // 60
        add_min = self.__duration % 60
        hour_ct  = self.__hour + add_hour - termin.hour
        min_ct   = self.__minute + add_min - termin.minute 
        new_duration = hour_ct*60 + min_ct
        return Term(termin.hour, termin.minute, new_duration)
