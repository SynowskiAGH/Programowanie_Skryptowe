from typing import List

from DeanerySystem.lesson import Lesson
from DeanerySystem.day import Day
from DeanerySystem.term import Term
from DeanerySystem.action import Action


class BasicTimetable:

    def __init__(self):
        self.lesson_dict = {}
    
    def put(self, lesson: Lesson) -> bool:
        if type(lesson) is not Lesson:
            raise TypeError('\'put()\' nie może być innego typu niż \'Lesson\'!')

        else:
            for les in list(self.lesson_dict.values()):
                if les.term == lesson.term:
                    raise ValueError(f'Podany termin nie jest dostępny!')
            self.lesson_dict[f'{lesson.term.printStartTime()}-{lesson.term.printEndTime()}-{lesson.term.day}'] = lesson
            
            return True


    def parse(self, actions: List[str]) -> List[Action]:
        action_list = []

        for ac in actions:
            if ac in Action._value2member_map_:
                action_list.append(Action(ac))
                
            else:
                raise ValueError(f'Tłumaczenie {ac} jest niepoprawne!')

        return action_list


    def get(self, term: Term) -> Lesson:
        ltr = None
        
        for les in list(self.lesson_dict.values()):
            if les.term == term:
                ltr = les
                break
        return ltr

    def perform(self, actions: List[Action]):
        x = 0
        for ac in actions:

            if ac == Action.DAY_EARLIER:
                list(self.lesson_dict.values())[x].earlierDay()

            elif ac == Action.DAY_LATER:
                list(self.lesson_dict.values())[x].laterDay()

            elif ac == Action.TIME_EARLIER:
                list(self.lesson_dict.values())[x].earlierTime()

            elif ac == Action.TIME_LATER:
                list(self.lesson_dict.values())[x].laterTime()

            x += 1
            x %= len(list(self.lesson_dict.values()))
