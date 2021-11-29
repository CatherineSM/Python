#4. Написати функцію < prime_list >, яка прийматиме 2 аргументи - початок і 
#кінець діапазона, і вертатиме список простих чисел всередині цього діапазона.

import math
 
def is_prime(i):
    m = min(i, int(math.sqrt(user_number2)))
    l = range(2, m)
    r = map(lambda x: i % x == 0, l)
    return not any(r)
 
user_number1 = int(input())
user_number2 = int(input())
ls = range(user_number1, user_number2)
ls2 = list(filter(is_prime, ls))
print(ls2)