'''\
Genegaciia i vivod chisel Fibonachi
'''

def fib(n):
    '''Vivodit posledovatelnost chisel Fibonachi, ne previshayshix n'''
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b

def fib2(n):
    '''Vozvrashaet spisok, sodergashiy chisla riada Fibonachi, ne previshayshix n'''
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a + b
    return result

