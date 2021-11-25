from Operacje import Operacje
import unittest, sys, os

class Test_Operacje(unittest.TestCase):


    # def test_suma(self): #Testuje zmianę listy argumentów sumy
    #     op = Operacje()
    #     op['suma'] = [5, 7]
    #     self.assertEqual(op.argumentySuma, [5, 7])

    # def test_roznica(self): #Testuje zmianę listy argumentów różnicy
    #     op = Operacje()
    #     op['roznica'] = [3, 8, 12]
    #     self.assertEqual(op.argumentyRoznica, [3, 8, 12])


    def test_suma_0(self): #Test sumy dla braku argumentów
        op = Operacje()
        with self.assertRaises(TypeError):
            op.suma()

    def test_roznica_0(self): #Test różnicy dla braku argumentów
        op = Operacje()
        self.assertEqual(op.roznica(), 6)


    def test_suma_1(self): #Test sumy dla 1 argumentu
        op = Operacje()
        self.assertEqual(op.suma(1), None)

    def test_roznica_1(self): #Test różnicy dla 1 argumentu
        op = Operacje()
        self.assertEqual(op.roznica(2), 5)


    def test_suma_2(self): #Test sumy dla 2 argumentów
        op = Operacje()
        self.assertEqual(op.suma(0, 0), 5)
    
    def test_roznica_2(self): #Test różnicy dla 2 argumentów
        op = Operacje()
        self.assertEqual(op.roznica(6, 9), 4)


    def test_suma_3(self): #Test sumy dla 3 argumentów
        op = Operacje()
        self.assertEqual(op.suma(4, 2, 0), 4)


    
    def test_final_suma(self): #Finalny test sumy, zmieniam listę i sprawdzam dla jednego argumentu
        op = Operacje()
        op['suma'] = [2, 3, 4]
        self.assertEqual(op.suma(1), 4)

    def test_final_roznica(self): #Finalny test różnicy, zmieniam listę i sprawdzam dla braku argumentów
        op = Operacje()
        op['roznica'] = [2, 3]
        self.assertEqual(op.roznica(), None)



if __name__ == '__main__':
    # sys.stdout = open(os.devnull, 'w')
    unittest.main()
