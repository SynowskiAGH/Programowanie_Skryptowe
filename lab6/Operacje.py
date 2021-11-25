from inspect import signature 

def argumenty(fargs): # -> fargs - ArgumentySuma/ArgumentyRoznica == [4, 5]/[4, 5, 6]

    def decorated_function(func): # Pobiera dekorowaną funkcję - w tym przypadku suma/różnica

        def decorated_arguments(*args): # Pobiera argumenty dekorowanej funkcji (self, x, y, (z))
            
            da_len = len(list(signature(func).parameters)) #Z podpisu funkcji func pobieram długość listy parametrów (długość funkcji suma argumentów)
            
            arg_list = list(args) # Lista argumentów
            
            req_len = len(arg_list) + len(fargs) # Dostępna ilość argumentów zapisanych i do dopisania


            if req_len < da_len: # Test czy dostępna ilość jest większa/równa wymaganej
                raise TypeError(
                    f'{func.__name__} bierze dokładnie {da_len-1} argumentów. ({req_len-1} argumentów pobranych.)') # - (-1) żeby odjąć selfa

            x = 0 #counter
            while len(arg_list) < da_len: # Dopisywanie argumentów
                arg_list.append(fargs[x]) 
                x += 1

            func(*arg_list) #wywołuję oryginalną funkcję z updejtowanymi argumentami

 
            try:
                return fargs[x]
            except:
                return None

        return decorated_arguments

    return decorated_function



class Operacje:
    argumentySuma = [4, 5]
    argumentyRoznica = [4, 5, 6]



    def __setitem__(self, op_word, value): # Wbudowana funkcja setitem, żeby można było zmienić wartości zmiennych przy użyciu odwołań do wartości tablicowych po indeksach (pog).
        if op_word == 'suma':
            
            self.argumentySuma = value # Nadpisuje value tablicy argumentySuma
            
            self.suma = (argumenty(self.argumentySuma))(self.no_dec_suma) # Redefiniuje funkcje suma
    

        elif op_word == 'roznica':
            
            self.argumentyRoznica = value # Nadpisuje value tablicy argumentyRoznica
            
            self.roznica = (argumenty(self.argumentyRoznica))(self.no_dec_roznica) # Redefiniuje funkcje roznica



    @argumenty(argumentySuma)
    def suma(self, x, y, z):
        print(f'{x} + {y} + {z} = {x + y + z}')

    def no_dec_suma(self, x, y, z):
        print(f'{x} + {y} + {z} = {x + y + z}')



    @argumenty(argumentyRoznica)
    def roznica(self, x, y):
        print(f'{x} - {y} = {x - y}')

    def no_dec_roznica(self, x, y):
        print(f'{x} - {y} = {x - y}')


if __name__ == '__main__':
    op = Operacje()
    op.suma(1, 2, 3)  # Wypisze: 1+2+3=6
    op.suma(1, 2)  # Wypisze: 1+2+4=7 - 4 jest pobierana z tablicy 'argumentySuma'
    op.suma(1)  # Wypisze: 1+4+5=10 - 4 i 5 są pobierane z tablicy 'argumentySuma'
    op.roznica(2, 1)  # Wypisze: 2-1=1
    op.roznica(2)  # Wypisze: 2-4=-2
    wynik = op.roznica()  # Wypisze: 4-5=-1
    print(wynik)  # Wypisze: 6
    op['suma'] = [1, 2]
    op['roznica'] = [1, 2, 3]
    print(op.argumentySuma)
    print(op.argumentyRoznica)
