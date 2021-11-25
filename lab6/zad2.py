import sys
from collections import Counter



# import sys; from collections import Counter; print(dict(Counter(map(lambda y: len(y), sys.stdin.read().split())).items()))



print(              # wypis
    dict(               # tworzymy słownik
            Counter(          # korzystamy z licznika i wyciągamy z niego krotki (długość, ilość)
                map(                 # dla każdego słowa w tablicy wykonujemy funkcję
                    lambda y: 
                    len(y),      # funkcja licząca długość podanego stringa
                    sys.stdin.read().split()    # wczytujemy dane z konsoli i rodzielamy je na słowa
                )
            ).items()
        )
    )
