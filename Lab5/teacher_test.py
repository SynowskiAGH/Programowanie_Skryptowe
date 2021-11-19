import unittest
from DeanerySystem import Day, Term, Lesson, Teacher, Timetable1 

class Test_TestTeacher(unittest.TestCase):

    def test_teacher(self): #Test działania stra
        teacher1 = Teacher('Piotr', 'Nowak')
        self.assertEqual(str(teacher1), 'Piotr Nowak')

    def test_lesson_init_teacher(self): #Test, czy pole teacher w lesson jest puste bez zdefiniowania go
        tt = Timetable1()
        les = Lesson(tt, Term(9, 35, Day.MON), "-", "-", 2)
        self.assertEqual(les.teacher, None)



    def test_add_hours(self): #Test dodawania godzin teachera
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        les + teacher1
        self.assertEqual(les.teacher.time, 90)

    def test_sub_hours(self): #Test usuwania godzin teacherowi
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        les + teacher1
        les - teacher1
        self.assertEqual(teacher1.time, 0)




    def test_add_teacher(self): #Test overloaded funkcji "add teacher"
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        les + teacher1
        self.assertEqual(les.teacher, teacher1)

    def test_sib_teacher(self): #Test overloaded funkcji "sub teacher"
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        les + teacher1
        les - teacher1
        self.assertEqual(les.teacher, None)




    def test_fill(self): #Test nadpisywania teachera
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        teacher2 = Teacher('Piotr Paweł', 'Nowak')
        les + teacher1
        les + teacher2
        self.assertEqual(les.teacher, teacher2)





    def test_add_to_limit(self): #Test dodawania DO limitu (poprawiło mi błąd!)
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        les2 = Lesson(tt, Term(17, 35, Day.WED), "-", "-", 2)
        les3 = Lesson(tt, Term(17, 35, Day.MON), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        les + teacher1
        les2 + teacher1
        les3 + teacher1
        self.assertEqual(teacher1.time, 270)

    def test_add_over_limit(self): #Test dodawania PONAD limit
        tt = Timetable1()
        les = Lesson(tt, Term(17, 35, Day.SUN), "-", "-", 2)
        les2 = Lesson(tt, Term(17, 35, Day.WED), "-", "-", 2)
        les3 = Lesson(tt, Term(17, 35, Day.MON), "-", "-", 2)
        les4 = Lesson(tt, Term(17, 35, Day.TUE), "-", "-", 2)
        teacher1 = Teacher('Piotr', 'Nowak')
        les + teacher1
        les2 + teacher1
        les3 + teacher1
        les4 + teacher1
        self.assertEqual(les4.teacher, None)



if __name__ == '__main__':
    unittest.main()
