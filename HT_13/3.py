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


