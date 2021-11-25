from functools import reduce
import re
import sys


print( # wypis
    len(  # liczymy długość listy
        list( # rzutowanie wyniku na listę
            filter(  # wybieramy tylko elementy z listy, które spełniają warunek postawiony w funkcji
                # funkcja sprawdzająca, czy podany argument zamieniony na liczbę jest parzysty
                lambda x: 
                int(x) % 2 == 0,

                    re.findall(r'\d+', # regex znajdujacy wszystkie liczby (jedna lub więcej cyfr)
                        
                        reduce( # połączenie wszystkich elementów listy zgodnie z funkcją
                            lambda x, y: x + y, # funkcja składająca każde dwa podane elementy w jeden
                                map( # wykonananie funkcji z każdym parametrem linii komend jako argumentem
                                    lambda x: 
                                    open(x, 'r').read(), #Otwieram każdy argv który podałem
                                    sys.argv[1:]
                                )
                        )
                    )
            )
        )
    )
)
