#1. Написати функцію < square > , яка прийматиме один аргумент - сторону 
#квадрата, і вертатиме 3 значення (кортеж): периметр квадрата, площа 
#квадрата та його діагональ.
from math import sqrt

user_number = int(input('Введите длину стороны квадрата'))

def square(user_number):
	if user_number <= 0:
		print 
	else:
		p_sqare = user_number ** 2
		s_sqare = user_number ** 3
		d_square = round(user_number * sqrt(2), 2)
		list1 = (p_sqare, s_sqare, d_square)
	return list1

if user_number > 0:
	print(tuple(square(user_number)))
else:
	print('Сторона квадрата должна быть больше 0')
