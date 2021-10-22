import re
import sys
from unittest.main import main


def main():
    while True:
        try:
            text = input()
            find(text)
        except KeyboardInterrupt:
            print('Error')
            break


def find(text):
    # for num in re.findall('[-]?[0-9]+):  
    #     yield int(num) - nieudana próba

    wrds = re.compile(r'[a-zA-Ząęćśżóę]+') #wszystkie slowa i znaki
    words = wrds.findall(text)
    
    numbrs = re.compile(r'\d+') #wszystkie liczby
    num = numbrs.findall(text)

    if num:
        print('Liczby:', ' '.join(num))
        
    if words: 
        print('Slowa:', ' '.join(words))
    

if __name__ == "__main__":
    main()
