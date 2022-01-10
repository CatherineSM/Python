class Calc:
    """Description
    Class has four methods for simple calculation with two numbers: additions, subtraction, multiplication & dividing.
    Result of each method saves in attribute last_result"""

    last_result = None

    def vadilate_number(self, num1, num2):
        if str(num1).isdigit() == False or str(num2).isdigit()== False:
            return print("Аргументы num1 и num2 должны быть числами")
        else:
            return (num1, num2)

    def numbers_sum(self, num1, num2):
        if self.vadilate_number(num1, num2) == False:
            return print("Аргументы num1 и num2 должны быть числами")
        else:
            Calc.last_result = num1 + num2
        return Calc.last_result

    def numbers_diff(self, num1, num2):
        if self.vadilate_number(num1, num2) == False:
            return print("Аргументы num1 и num2 должны быть числами")
        else:
            Calc.last_result = num1 - num2
        return Calc.last_result

    def numbers_multiple(self, num1, num2):
        if self.vadilate_number(num1, num2) == False:
            return print("Аргументы num1 и num2 должны быть числами")
        else:
            Calc.last_result = num1 * num2
        return Calc.last_result

    def numbers_division(self, num1, num2):
        if self.vadilate_number(num1, num2) == False:
            return print("Аргументы num1 и num2 должны быть числами")
        elif num2 == 0:
            return print("Делить на 0 нельзя")
        else:
            Calc.last_result = num1 / num2
        return Calc.last_result

example = Calc()
print(example.numbers_sum(7, 7))
print(example.last_result)
print(example.numbers_multiple(7, 7))
print(example.last_result)