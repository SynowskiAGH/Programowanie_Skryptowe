import sys
import re

print(
    
    *list( # Wypisujemy listy po indeksie

        map( # Nadajemy daną funkcję na każdy item

            lambda y: list(y.group()), # Łącze zesplitowane iteracje tego samego znaku w listę

                re.finditer(r'(.)\1*', "".join( # (.)\1* -> matchuje każdy (.) znak, który jest taki sam jak poprzedni (\1), tyle razy ile potrzeba (*) i łącze je w stringa

                    "".join( # Łączenie listy w string (np.: 121112)
                        
                        list( #robimy z nich listę
                            
                            map( # Nadajemy daną funkcję na każdy 'item' -> każdy zesplitowany 'wyraz' (liczbę)
                                lambda y: y.rstrip(), sys.argv[1:]) # Usuwamy wszystkie białe znaki z inputu
        
                                    )).split(",") # Splitujemy input po przecinkach
                ))
        )
    )
)
