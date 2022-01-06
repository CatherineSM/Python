#3. Напишіть програму, де клас «геометричні фігури» (figure) містить властивість color з початковим значенням white і 
#метод для зміни кольору фігури, а його підкласи «овал» (oval) і «квадрат» (square) містять методи init для завдання 
#початкових розмірів об'єктів при їх створенні.

class Shape:

    def __init__(self):
        self.color = "White"

    def set_color(self, color):
        self.color = color


class Square(Shape):

    def __init__(self, height, width):
        Shape.__init__(self)
        self.height = height
        self.width = width


class Oval(Shape):

    def __init__(self, height, width):
        Shape.__init__(self)
        self.height = height
        self.width = width


shape = Shape()
square = Square(1, 2)
oval = Oval(3, 4)
oval.set_color("Black")

print(shape.__dict__)
print(square.__dict__)
print(oval.__dict__)


