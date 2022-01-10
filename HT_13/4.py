class Shape:

    def __init__(self, color):
        self.color = color

    def set_color(self, color):
        self.color = color


class Square(Shape):

    def __init__(self, color, height, width):
        super().__init__(color)
        self.height = height
        self.width = width


class Oval(Shape):

    def __init__(self, color, height, width):
        super().__init__(color)
        self.height = height
        self.width = width


shape = Shape("Red")
square = Square("Green", 1, 2)
oval = Oval("Blue", 3, 4)

print(shape.__dict__)
print(square.__dict__)
print(oval.__dict__)


