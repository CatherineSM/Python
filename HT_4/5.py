#5. Написати функцію < fibonacci >, яка приймає один аргумент і виводить 
#всі числа Фібоначчі, що не перевищують його.

user_number = int(input())

def fibonacci(user_number):
    fibn= [0,1] 
    while fibn[-1] < user_number:
        fibn.append(fibn[-1]+fibn[-2])
    return fibn

list1 = fibonacci(user_number)
list1.pop(-1)
print (list1)