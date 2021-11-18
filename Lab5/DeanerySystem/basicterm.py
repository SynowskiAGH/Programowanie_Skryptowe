from DeanerySystem.day import Day

class BasicTerm():
    def __init__(self, hour, minute, duration=90):
        self.__hour = hour
        self.__minute = minute
        self.__duration = duration

    @property
    def hour(self):
        return self.__hour

    @hour.setter
    def hour(self, value):
        if type(value) is not int:
            raise TypeError('Godzina musi być liczbą całkowitą')
        elif value < 0 or value > 23:
            raise ValueError('Godzina musi należeć do przedziału 0 - 23')
        else:
            self.__hour = value

    @property
    def minute(self):
        return self.__minute

    @minute.setter
    def minute(self, value):
        if type(value) is not int:
            raise TypeError('Minuta musi być liczbą całkowitą')
        elif value < 0 or value > 59:
            raise ValueError('Minuta musi należeć do przedziału 0 - 59')
        else:
            self.__minute = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if type(value) is not int:
            raise TypeError('Duration musi być liczbą całkowitą')
        elif value <=0:
            raise ValueError('Duration musi być dodatnie')
        else:
            self.__duration = value

    def __lt__(self, other):
        return self.earlierThan(self, other)

    def __le__(self, other):
        return self.earlierThan(self, other) or self.equals(self, other)

    def __eq__(self, other):
        return self.equals(self, other)

    def __ge__(self, other):
        return self.laterThan(self, other) or self.equals(self, other)

    def __gt__(self, other):
        return self.laterThan(self, other)


    def getStartTime(self):
        return (self.hour, self.minute)

    def getEndTime(self):
        add_hour = self.__duration // 60
        add_min = self.__duration % 60
        end_min = self.__minute + add_min

        if end_min >= 60:
            add_hour += 1
            end_min %= 60

        end_hour = self.__hour + add_hour

        return (end_hour, end_min)
    
    def getCompTime(self):
        et = self.getEndTime()
        return (self.hour, self.minute, et[0], et[1])

    def printEndTime(self):
        timeTuple = self.getEndTime()
        return f'{timeTuple[0]:0>2}:{timeTuple[1]:0>2}'

    def printStartTime(self):
        return f'{self.__hour:0>2}:{self.__minute:0>2}'

    def __str__(self):
        return(f"{self.__hour}:{self.__minute} [{self.__duration}]")

    def laterThan(self, Termin):
        if Day.difference(self.__day, Termin.day) < 0:
            return True
        if Day.difference(self.__day, Termin.day) == 0:
            if Termin.hour < self.__hour:
                return True
            elif Termin.hour == self.__hour and Termin.minute < self.__minute:
                return True
            return False
        return False

    def equals (self, Termin):
        return True if Day.difference(self.__day, Termin.day) == 0 and Termin.__hour == self.__hour and Termin.__minute == self.__minute and Termin.__duration == self.__duration else False
    
    def earlierThan(self, Termin):
        if Day.difference(self.__day, Termin.day) > 0:
            return True
        elif Day.difference(self.__day, Termin.day) == 0:
            if Termin.hour > self.__hour:
                return True
            elif Termin.hour == self.__hour and Termin.minute > self.__minute:
                return True
            return False
        return False
