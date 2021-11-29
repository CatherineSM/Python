#3. Написати функцию < is_prime >, яка прийматиме 1 аргумент - число від 0 
#до 1000, и яка вертатиме True, якщо це число просте, и False - якщо ні.

from math import sqrt

user_number = int(input('Введите число: '))

def is_prime(number):
    if number % 2 == 0 and number != 2:
        return False
    if number == 0 or number == 1:
        return False
    for n in range(3, int(sqrt(number).real)):
        if number % user_number == 0: 
            return False
    return True  

print(is_prime(user_number))
