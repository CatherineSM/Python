#3. Написати функцiю season, яка приймає один аргумент — номер мiсяця (вiд 1 
#до 12), яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, 
#лiто або осiнь)

def season (m):
    if m == 12 or m == 1 or m == 2:
        return 'Зима'
    elif m == 3 or m == 4 or m == 5:
        return 'Весна'
    elif m == 6 or m == 7 or m == 8:
        return 'Лето'
    elif m == 9 or m == 10 or m == 11:
        return 'Осень'
    elif m == 0 or m > 12:
        return 'Введите число от 1 до 12'

result = season (int(input('Введите номер месяца: ')))

print (result)