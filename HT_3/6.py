user_string = input('Введите любые символы')

leters = []
numbers_sum = ()
numbers = ()
letters = ()

for symbol in user_string:
    if symbol.isdigit():
        numbers_sum += int(symbol)
        numbers += 1
    elif symbol.isalpha()
        leters += symbol
        letters += 1

if len(user_string) < 30:
    print('Сумма чисел ', numbers_sum)
    print('Только буквы', ''.join(leters))

elif len(user_string) < 50:
    print('Длина строки ', len(user_string))
    print('Цифры ', numbers)
    print('Буквы ', numbers)

else:
    print('И этого хватит))')


