from DeanerySystem.term import Term


class Lesson:
    def __init__(self, term: Term, name: str, teacherName: str, year: int, fullTime: bool):
        self.term = term
        self.name = name
        self.teacherName = teacherName
        self.year = year
        self.fullTime = self.isFullTime() #Tak wywołujesz z selfem

    def isFullTime(self):
        if self.term._day.value in range (1,4): return True
        if self.term._day.value == 5 and self.hour in range (8-17):
            return True
        return False

    def earlierDay(self):
        if self.fullTime == True: #Dla FullTerm
            if 2 <= self.term._day.value <= 5:
                self.term._day.value = self.term._day.value - 1
                return True
        else: #Dla NotFullTerm
            if 6 <= self.term._day.value <= 7:
                self.term._day.value = self.term._day.value - 1
                return True
        return False

    def laterDay(self):
        if self.fullTime == True: #Dla FullTerm
            if 1 <= self.term._day.value <=4:
                self.term._day.value = self.term._day.value + 1
                return True
        else: #Dla NotFullTerm
            if 5 <= self.term._day.value <= 6:
                self.term._day.value = self.term._day.value + 1
                return True
        return False


    def earlierTime(self, duration):
        h_dif = self.term.duration // 60
        m_dif = self.term.duration % 60

        if self.fullTime == True:
            new_hour = self.term.hour + h_dif
            new_min = self.term.hour + m_dif
            if new_hour in range (8-19)
        pass

    def laterTime():
        if self.fullTime == True:
            
            new_hour = self.term.hour + 
        pass        
        pass

    def __str__():
        pass
