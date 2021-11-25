#7. Ну і традиційно -> калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 
#аргументи - один з яких операцiя, яку зробити!

user_num1 = int(input('Введите первое число')) 
user_num2 = int(input('Введите второе число')) 
operator = input('Введите знак операции (*, +, - или /)')

def arithmetic(user_num1, user_num2, operator):
    if operator == '+':
        return user_num1 + user_num2
    elif operator == '-':
        return user_num1 - user_num2
    elif operator == '*':
        return user_num1 * user_num2
    elif operator == '/':
        return user_num1 / user_num2
    else:
        return "Неизвестная операция"

result = arithmetic(user_num1, user_num2, operator)
print(result)