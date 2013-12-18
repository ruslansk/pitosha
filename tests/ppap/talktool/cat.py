# cat.py

class Cat(object):
    def __init__(self, name='Tom'):
        self.name = name

    def eat(self, food):
        if food == 'fish':
            return 'Yummy!'
        else:
            return 'Ugh!'
