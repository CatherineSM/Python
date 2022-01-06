class Calc:
	last_result = None

	def numbers_sum (self, num1, num2):
		if str(num1).isdigit() == False or str(num2).isdigit() == False:
			return print("Аргументы num1 и num2 должны быть числами")
		else:
			Calc.last_result = num1 + num2
		return Calc.last_result

	def numbers_diff (self, num1, num2):
		if str(num1).isdigit() == False or str(num2).isdigit() == False:
			return print("Аргументы num1 и num2 должны быть числами")
		else:
			Calc.last_result = num1 - num2
		return Calc.last_result

	def numbers_product (self, num1, num2):
		if str(num1).isdigit() == False or str(num2).isdigit() == False:
			return print("Аргументы num1 и num2 должны быть числами")
		else:
			Calc.last_result = num1 * num2
		return Calc.last_result

	def numbers_division (self, num1, num2):
		if str(num1).isdigit() == False or str(num2).isdigit() == False:
			return print("Аргументы num1 и num2 должны быть числами")
		elif num2 == 0:
			return print("Делить на 0 нельзя")
		else:
			Calc.last_result = num1 / num2
		return Calc.last_result

example = Calc()
print(example.numbers_division(7, 7))
print(example.last_result)
print(example.numbers_product(7, 7))
print(example.last_result)