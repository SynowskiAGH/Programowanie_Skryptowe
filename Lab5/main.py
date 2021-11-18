from DeanerySystem import Day, Term, Lesson, Action, Timetable1

term1 = Term(15, 0, Day.WED)
term2 = Term(15, 0, Day.FRI)
term3 = Term(13, 30, Day.SAT)
term4 = Term(11, 0, Day.MON)

tt1 = Timetable1()

Polski = Lesson(tt1, term1, 'Polski','polski', 2)
Angielski = Lesson(tt1, term2, 'Angielski', 'angielski', 2)
Przyrka = Lesson(tt1, term3, 'Przyrka', 'przyrka', 2)
Fizyka = Lesson(tt1, term4, 'Fizyka', 'fizyka', 2)


print(tt1)

tt1.put(Polski)
tt1.put(Angielski)
tt1.put(Przyrka)
tt1.put(Fizyka)

print(tt1)

tt1.perform(tt1.parse(['d+', 'd+', 'd+', 'd+']))

print(tt1)
