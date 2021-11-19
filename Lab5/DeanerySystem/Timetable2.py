from typing import List
from DeanerySystem.break_class import Break

from DeanerySystem.day import Day
from DeanerySystem.term import Term
from DeanerySystem.lesson import Lesson
from DeanerySystem.action import Action
from DeanerySystem.basictimetable import BasicTimetable


class Timetable2(BasicTimetable):
    skipBreaks = False

    """ Class containing a set of operations to manage the timetable """

    def __init__(self, breaks: List[Break]):
        super().__init__()
        self.breaks = breaks

    def overlapsBreak(self, term: Term) -> bool: #Check overlapu
        start_time = term.getStartTime()
        end_time = term.getEndTime()

        for bre in self.breaks:
            break_start = bre.term.getStartTime()
            break_end = bre.term.getEndTime()

            if start_time > break_start and start_time < break_end:
                return (True, bre.term.duration)

            if end_time > break_start and end_time < break_end:
                return (True, bre.term.duration)

            if start_time == break_start and end_time > break_end:
                return (True, bre.term.duration)
                
            if start_time < break_start and end_time == break_end:
                return (True, bre.term.duration)

        return False


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

        if term.hour < 8:
            return False

        et = term.getEndTime()
        if et[0] > 20:
            return False
        if et[0] == 20 and et[1] > 0:
            return False

        if not self.busy(term):

            if term.day.value < 5:
                is_FullTime = True
            elif term.day.value > 5:
                is_FullTime = False

            else:
                if term.hour < 17:
                    is_FullTime = True
                else:
                    is_FullTime = False

            if is_FullTime == full_time:
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

        for les in list(self.lesson_dict.values()):
            if les.term == term:
                return True

            les_start = (les.term.hour, les.term.minute)
            les_end = les.term.getEndTime()
            ter_start = (term.hour, term.minute)
            ter_end = term.getEndTime()

            if les_end > ter_start and les_end < ter_end:
                return True
            if ter_end > les_start and ter_end < les_end:
                return True
            if les_start > ter_start and les_start < ter_end:
                return True
            if ter_start > les_start and ter_start < les_end:
                return True

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
            for les in list(self.lesson_dict.values()):
                if les.term == lesson.term:
                    raise ValueError(f'Podany termin jest zajęty przez inną lekcję')

            if self.overlapsBreak(lesson.term):
                raise ValueError('Podany termin jest zajęty przez przerwę')

            self.lesson_dict[f'{lesson.term.printStartTime()}-{lesson.term.printEndTime()}-{lesson.term.day}'] = lesson
            return True


    def __str__(self):
        timetable = [] #Wywołuje tablice timetable
        space = ''
        line = f'\n{space: ^12}{space:*^92}\n'

        for les in list(self.lesson_dict.values()):
            timetable.append(les.term)

        for bre in self.breaks:
            t_string = f'{bre.term.printStartTime()}-{bre.term.printEndTime()}'
            if not t_string in timetable:
                timetable.append(t_string)
        timetable = sorted(timetable)

        displaytable = []
        for i in range(8):
            displaytable.append([])
            for j in range(len(timetable) + 1):
                displaytable[i].append('')      

        for c, t in enumerate(timetable):
            displaytable[0][c + 1] = f'{t.printStartTime()}-{t.printEndTime()}'

        for d in Day:
            displaytable[d.value][0] = str(d)

        for les in list(self.lesson_dict.values()):
            t_string = f'{les.term.printStartTime()}-{les.term.printEndTime()}'            
            displaytable[les.term.day.value][timetable.index(les.term) + 1] = les.name

        for bre in self.breaks:
            t_string = f'{bre.term.printStartTime()}-{bre.term.printEndTime()}'
            for i in range(1, 8):
                displaytable[i][timetable.index(t_string) + 1] = f'------'

        return_string = ''
        for tc in range(len(timetable) + 1):
            for dc in range(8):
                return_string += f'{displaytable[dc][tc]: ^12}*'
            return_string += line

        return return_string
        
