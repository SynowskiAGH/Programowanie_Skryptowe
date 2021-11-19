
import unittest
from DeanerySystem import Day, Term, Lesson, Action, Timetable1 

class Test_TestIncrementDecrement(unittest.TestCase):

    def test_put(self): #Test puta
        tt = Timetable1()
        les = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        self.assertEqual(tt.put(les), True)

    def test_put_false(self): #Test failu puta
        tt = Timetable1()
        les = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.put(les), False)




    def test_get(self): #Test geta
        tt = Timetable1()
        ter1 = Term(9, 30, Day.THU)
        les = Lesson(tt, ter1, "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.get(ter1), les)

    def test_get_fail(self): #Test breaku geta
        tt = Timetable1()
        ter1 = Term(9, 30, Day.THU)
        les = Lesson(tt, ter1, "-", "-", 2)
        self.assertEqual(tt.get(les), None)




    def test_busy(self): #Test stanu busy
        tt = Timetable1()
        les = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.busy(les.term), True)

    def test_busy_2(self):#Test overlapu busy
        tt = Timetable1()
        les = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        ter1 = Term(9, 00, Day.THU)
        tt.put(les)
        self.assertEqual(tt.busy(ter1), True)

    def test_busy_fail(self): #Test failu busy - dla pustego terminu
        tt = Timetable1()
        les = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        self.assertEqual(tt.busy(les.term), False)




    def test_canbetransfered(self): #Test dla full term - poprawny
        tt = Timetable1()
        ter1 = Term(9, 30, Day.THU)
        ter2 = Term(11, 00, Day.THU)
        les = Lesson(tt, ter1, "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.can_be_transferred_to(ter2, True), True)

    def test_cbtt_ft_false(self): #Test dla full term - niepoprawny
        tt = Timetable1()
        ter1 = Term(9, 30, Day.THU)
        ter2 = Term(11, 00, Day.SAT)
        les = Lesson(tt, ter1, "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.can_be_transferred_to(ter2, True), False)



    def test_canbetransfered_notfullterm(self): #Test dla not full term - poprawny
        tt = Timetable1()
        ter1 = Term(9, 30, Day.SAT)
        ter2 = Term(11, 00, Day.SAT)
        les = Lesson(tt, ter1, "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.can_be_transferred_to(ter2, False), True)

    def test_canbetransfered_notfullterm_fail(self): #Test dla not full term - failowy
        tt = Timetable1()
        ter1 = Term(9, 30, Day.SAT)
        ter2 = Term(11, 00, Day.THU)
        les = Lesson(tt, ter1, "-", "-", 2)
        tt.put(les)
        self.assertEqual(tt.can_be_transferred_to(ter2, False), False)




    def test_parse(self): #Test poprawności parse
        tt = Timetable1()
        strl = ['d-', 'd+', 't-', 't+']
        actl = [Action.DAY_EARLIER, Action.DAY_LATER, Action.TIME_EARLIER, Action.TIME_LATER]
        self.assertEqual(tt.parse(strl), actl)




    def test_peform(self): #Test poprawności performa
        tt = Timetable1()
        tt1 = Timetable1()
        ter2 = Term(8, 0, Day.WED)
        les1 = Lesson(tt1, ter2, 'less1', 'less1', 2)
        actl = [Action.DAY_EARLIER, Action.DAY_LATER, Action.TIME_EARLIER, Action.TIME_LATER]
        tt.put(les1)
        tt1.put(les1)
        tt1.perform(actl)
        self.assertEqual(tt1.lesson_list, tt.lesson_list)


if __name__ == '__main__':
    unittest.main()
