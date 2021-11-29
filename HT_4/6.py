#6. Вводиться число. Якщо це число додатне, знайти його квадрат, якщо від'ємне,
# збільшити його на 100, якщо дорівнює 0, не змінювати.

user_number = int(input())

if user_number > 0:
	print(user_number ** 2)
elif user_number < 0:
	print(user_number + 100)
elif user_number == 0:
	print(user_number)