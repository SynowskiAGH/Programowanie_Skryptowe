import unittest
from DeanerySystem import Day, Term, Lesson, Action, Break, BasicTerm, Timetable2 

class Test_Timetable2(unittest.TestCase):

    def test_put_true (self): #Test na "def put" - test zwracania True dla dobrych danych
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        les = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        self.assertEqual(tt.put(les), True) #Lekcja slotuje się między przerwami

    def test_put_false(self): #Test na "def put" - zwracanie False
        b = [Break(BasicTerm(11, 5, 10)), Break(BasicTerm(12, 45, 10))]
        tt = Timetable2(b)
        les0 = Lesson(tt, Term(11, 10, Day.THU), "-", "-", 2)
        with self.assertRaises(ValueError):
            tt.put(les0) #Lekcja znajduje się w slocie przerwy i zwraca error

    def test_get(self): #Test na "def get" - lekcji, która może się odbyć
        b = [Break(BasicTerm(11, 5, 10)), Break(BasicTerm(12, 45, 10))]
        tt = Timetable2(b)
        ter0 = Term(11, 15, Day.THU)
        les0 = Lesson(tt, ter0, "-", "-", 2)
        tt.put(les0)
        self.assertEqual(tt.get(ter0), les0)

    def test_get_false(self): #Test na "def get" - lekcji, która nie może się odbyć
        b = [Break(BasicTerm(11, 15, 10)), Break(BasicTerm(12, 55, 10))]
        tt = Timetable2(b)
        ter0 = Term(11, 20, Day.FRI)
        les0 = Lesson(tt, ter0, "-", "-", 2)
        self.assertEqual(tt.get(les0), None)

    def test_busy(self): #Test na "def busy" - busy lekcji
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        les0 = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        tt.put(les0)
        self.assertEqual(tt.busy(les0.term), True)

    def test_busy_fail(self): #Test na "def busy" - lekcja nie odbywa się
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        les0 = Lesson(tt, Term(9, 35, Day.THU), "-", "-", 2)
        self.assertEqual(tt.busy(les0.term), False)

    def test_cbtt_ft_true(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        ter0 = Term(9, 35, Day.THU)
        ter = Term(11, 15, Day.THU)
        les0 = Lesson(tt, ter0, "-", "-", 2)
        tt.put(les0)
        self.assertEqual(tt.can_be_transferred_to(ter, True), True)

    def test_cbtt_ft_false(self): #TESTOWANIE CBT? - SUSSY BAKA
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        ter0 = Term(9, 35, Day.THU)
        ter = Term(11, 15, Day.SAT)
        les0 = Lesson(tt, ter0, "-", "-", 2)
        tt.put(les0)
        self.assertEqual(tt.can_be_transferred_to(ter, True), False)

    def test_cbtt_nft_true(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        ter0 = Term(9, 35, Day.SAT)
        ter = Term(11, 15, Day.SAT)
        les0 = Lesson(tt, ter0, "-", "-", 2)
        tt.put(les0)
        self.assertEqual(tt.can_be_transferred_to(ter, False), True)

    def test_cbtt_nft_false(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        ter0 = Term(9, 35, Day.SAT)
        ter = Term(11, 15, Day.THU)
        les0 = Lesson(tt, ter0, "-", "-", 2)
        tt.put(les0)
        self.assertEqual(tt.can_be_transferred_to(ter, False), False)

    def test_parase(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        strl = ['d-', 'd+', 't-', 't+']
        actl = [Action.DAY_EARLIER, Action.DAY_LATER, Action.TIME_EARLIER, Action.TIME_LATER]
        self.assertEqual(tt.parse(strl), actl)

    def test_parase_value_error(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        strl = ['d-', 'd+', 't-', 't+', 'catch me']
        actl = [Action.DAY_EARLIER, Action.DAY_LATER, Action.TIME_EARLIER, Action.TIME_LATER]
        with self.assertRaises(ValueError):
            tt.parse(strl)

    def test_peform_skipBreakFalse(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        tt1 = Timetable2(b)
        ter = Term(8, 0, Day.WED)
        les1 = Lesson(tt1, ter, 'less1', 'less1', 2)
        actl = [Action.DAY_EARLIER, Action.DAY_LATER, Action.TIME_EARLIER, Action.TIME_LATER]
        tt.put(les1)
        tt1.skipBreaks = False
        tt1.put(les1)
        tt1.perform(actl)
        self.assertEqual(tt1.lesson_dict, tt.lesson_dict)

    def test_peform_skipBreakTrue(self):
        b = [Break(BasicTerm(9, 30, 5)), Break(BasicTerm(11, 5, 10))]
        tt = Timetable2(b)
        tt1 = Timetable2(b)
        ter = Term(8, 0, Day.WED)
        les1 = Lesson(tt1, ter, 'less1', 'less1', 2)
        actl = [Action.DAY_EARLIER, Action.DAY_LATER, Action.TIME_EARLIER, Action.TIME_LATER]
        tt.put(les1)
        tt1.skipBreaks = True
        tt1.put(les1)
        tt1.perform(actl)
        self.assertEqual(tt1.lesson_dict, tt.lesson_dict)



if __name__ == '__main__':
    unittest.main()
