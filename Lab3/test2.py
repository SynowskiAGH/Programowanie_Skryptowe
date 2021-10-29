import unittest
from DeanerySystem.day import Day
from DeanerySystem.term import Term
import unittest

class Test_DSystem(unittest.TestCase):
    global term1, term2, term3
    term1 = Term(Day.TUE, 9, 45)
    term2 = Term(Day.WED, 10, 15)
    term3 = Term(Day.TUE, 11, 15)

    def test_earlier(self):
        self.assertEqual(term1.earlierThan(term2), True)
        self.assertEqual(term2.earlierThan(term1), False)

    def test_later(self):
        self.assertEqual(term1.laterThan(term2), False)
        self.assertEqual(term2.laterThan(term1), True)
        
    def test_equal(self):
        self.assertEqual(term1.equals(term2), False)
        self.assertEqual(term1.equals(term3), False)

    def test_represent(self):
        self.assertEqual(term1.__str__(), "Wtorek 9:45 [90]")
        self.assertEqual(term2.__str__(), "Środa 10:15 [90]")
        self.assertEqual(term3.__str__(), "Wtorek 11:15 [90]")

if __name__ == '__main__':
    unittest.main()
