def sum(arg1, arg2):
    x = arg1 + arg2 
    return x

if(__name__ == '__main__'):
    print(sum(1,3))
    print( "__name__ =", __name__)
else:
    print(__name__)
