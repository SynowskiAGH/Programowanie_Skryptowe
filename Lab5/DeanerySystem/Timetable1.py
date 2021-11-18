from typing import List

from DeanerySystem.day import Day
from DeanerySystem.term import Term
from DeanerySystem.lesson import Lesson
from DeanerySystem.action import Action


class Timetable1:
    """ Class containing a set of operations to manage the timetable """

    def __init__(self):
        self.lesson_list = []

    def can_be_transferred_to(self, term: Term, full_time: bool) -> bool:
        """
        Informs whether a lesson can be transferred to the given term
        Parameters
        ----------
        term : Term
            The term checked for the transferability
        full_time : bool
            Full-time or part-time studies
        Returns
        -------
        bool
            **True** if the lesson can be transferred to this term
        """

        if term.hour < 8: #Jeśli zaczyna się przed 8
            return False

        et = term.getEndTime()
        if et[0] > 20: #Jeśli kończy się po 20
            return False
        if et[0] == 20 and et[1] > 0:
            return False

        if not self.busy(term):
            if term.day.value < 5: #Jeśli pon-piątek full term
                is_ft = True
            elif term.day.value > 5: #sob-nie nie full term
                is_ft = False
            else:
                if term.hour < 17: #przed 17
                    is_ft = True
                else:
                    is_ft = False  #po 17

            if is_ft == full_time:
                return True
        return False

    def busy(self, term: Term) -> bool:
        """
        Informs whether the given term is busy.  Should not be confused with ``can_be_transfered_to()``
        since there might be free term where the lesson cannot be transferred.
        Parameters
        ----------
        term : Term
            Checked term
        Returns
        -------
        bool
            **True** if the term is busy
        """

        for les in self.lesson_list:
            if les.term == term: #Jeśli lekcja pokrywa się z term to zwracamy True
                return True

            les_start = (les.term.hour, les.term.minute) #Godzina rozpoczęcia się termu
            les_end = les.term.getEndTime() #Godzina zakończenia się termu
            ter_start = (term.hour, term.minute) #Godzina rozpoczęcia się lekcji
            ter_end = term.getEndTime() #Godzina zakończenia się lekcji

            if les_end > ter_start and les_end < ter_end:
                return True #Jeśli lekcja znajduje się wokół termu to true
            if ter_end > les_start and ter_end < les_end:
                return True #Jeśli lekcja znajduje się wewnątrz termu to true
            if les_start > ter_start and les_start < ter_end:
                return True #Jeżel lekcja otwarta od lewej zamknięta od prawej
            if ter_start > les_start and ter_start < les_end:
                return True #Jeżeli otwarta od prawej, zamknięta od lewej

        return False

    def put(self, lesson: Lesson) -> bool:
        """
        Add the given lesson to the timetable.
        Parameters
        ----------
        lesson : Lesson
            The added  lesson
        Returns
        -------
        bool
            **True**  if the lesson was added.  The lesson cannot be placed if the timetable slot is already occupied.
        """

        if type(lesson) is not Lesson:
            raise TypeError('Argument \'put()\' musi być typu \'Lesson\'')
        else:
            if self.busy(lesson.term):
                return False
            self.lesson_list.append(lesson) 
            return True #Jeśli nie jest busy to dodajemy i zwracamy true 


    def parse(self, actions: List[str]) -> List[Action]:
        """
        Converts an array of strings to an array of 'Action' objects.
        Parameters
        ----------
        actions:  List[str]
            A list containing the strings: "d-", "d+", "t-" or "t+"
        Returns
        -------
            List[Action]
                A list containing the values:  DAY_EARLIER, DAY_LATER, TIME_EARLIER or TIME_LATER
        """

        action_list = []
        for ac in actions:
            if ac in Action._value2member_map_: #Jeśli ac znajduje się w liście stringów z action.py
                action_list.append(Action(ac)) #Zapisz ac do listy akcji
        return action_list

    def perform(self, actions: List[Action]):
        """
        Transfer the lessons included in the timetable as described in the list of actions. N-th action should be sent the n-th lesson in the timetable.
        Parameters
        ----------
        actions : List[Action]
            Actions to be performed
        """
        lc = 0
        for ac in actions: #Wybieramy z listy akcji
            if ac == Action.DAY_EARLIER:
                self.lesson_list[lc].earlierDay()
            elif ac == Action.DAY_LATER:
                self.lesson_list[lc].laterDay()
            elif ac == Action.TIME_EARLIER:
                self.lesson_list[lc].earlierTime()
            elif ac == Action.TIME_LATER:
                self.lesson_list[lc].laterTime()

            lc += 1 #+1 pozycja w liście
            lc %= len(self.lesson_list) #Powrót do zerowej pozycji (gdyby ac było dłuższe od lc)

    def __str__(self):
        timetab = [] #tworzę timetab
        for les in self.lesson_list: 
            timetab.append(les.term) #Iteruje przez lekcje i dodaje do timetaba czas ich rozpoczęcia
        timetab = sorted(timetab, key=lambda t: t.printStartTime()) #Sortuje przez godzinę rozpoczęcia

        disptab = [] #Tablica display
        for i in range(8): # 1-7
            disptab.append([])
            for j in range(len(timetab) + 1): # 1-(n+1)godzin w timetab
                disptab[i].append('') # ??? Puste pole dla disptab X = [1 - 7] ???
        
        for d in Day: #Wypisuje dni tygodnia jako pole X tablicy 2-wymiarowej (1|0-pon, 2|0-wt, 3|0-sr itd.)
            disptab[d.value][0] = str(d)

        for c, t in enumerate(timetab): #iteruje po możliwych terminach -> 0 - pierwszy termin(c i t na raz czy oddzielnie?)
            disptab[0][c + 1] = f'{t.printStartTime()}-{t.printEndTime()}' #od [0][1] wpisuje odpowiednio starttime i endtime

        for les in self.lesson_list: #Dla każdej lekcji w liście
            disptab[les.term.day.value][timetab.index(les.term) + 1] = les.name #disptab[1][index posortowanego terma+1] <- nazwa lekcji

        b = '' # spacja
        bl = f'\n{b: ^12}{b:*^92}\n' # bl -> 12 przerw i 92 gwiazdki :3
        em = f'{b: ^12}' # em? nie widzi tego lmao?

        finstr = '' #finished string (?)
        for tc in range(len(timetab) + 1): #Dla każdego czasu w liście timetab:
            for dc in range(8): #Dla każdego dnia:
                finstr += f'{disptab[dc][tc]: ^12}*' # ^ - centrowanie zawartości tablicy (width=12) - gwiazdka na koniec
            finstr += bl #Co każdy term dodaje linie

        return finstr #zwraca finstr
        

    def get(self, term: Term) -> Lesson: #funckja getująca
        """
        Get object (lesson) indicated by the given term.
        Parameters
        ----------
        term: Term
            Lesson date
        Returns
        -------
        lesson: Lesson
            The lesson object or None if the term is free
        """
        
        ltr = None
        for les in self.lesson_list:
            if les.term == term:
                ltr = les
                break
        return ltr
