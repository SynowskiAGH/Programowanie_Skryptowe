from fractions import Fraction

def sum(arg1, arg2):
    if (type(arg1) or type(arg2)) is complex:
        return complex(arg1.real + arg2.real, arg1.imag + arg2.imag)

    elif (type(arg1) or type(arg2)) is Fraction:
        return Fraction(arg1 + arg2)

    # elif (type(arg1) or type(arg2)) is str:
    #      return float(arg1) + float(arg2) - Wszystko zamyka się w
    #      jednym elsie

    else:
        return float(arg1) + float(arg2)

if(__name__ == '__main__'):
    print(sum(1,3))
    print( "__name__ =", __name__)
else:
    print(__name__)
