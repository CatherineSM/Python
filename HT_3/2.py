#2. Користувачем вводиться початковий і кінцевий рік. Створити цикл, який 
#виведе всі високосні роки в цьому проміжку (границі включно).

start_year = int(input("Введите год начала отсчета"))
end_year = int(input("Введите год окончания отсчета"))

list1 = []
for i in range(start_year, end_year + 1):
    if i % 400 == 0:
        list1.append(i)
    elif i % 4 == 0 and i % 100 != 0:
        list1.append(i)

print('Высокосные года в указанном промежутке:', list1)
