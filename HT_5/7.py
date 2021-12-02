#7. Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну 
#послідовність (рядок, список, кортеж) і повертає генератор, який буде 
#вертати значення з цієї послідовності, при цьому, якщо було повернено 
#останній елемент із послідовності - ітерація починається знову.
#   Приклад (якщо запустили його у себе - натисніть Ctrl+C ;) ):
#   >>>for elem in generator([1, 2, 3]):
#   ...    print(elem)
from itertools import cycle

usur_input=input("Введите значения через кому")
a_list = list(query.split(',')) 

from itertools import cycle

def yes_no(a_list):
   return itertools.cycle(a_list)

print(a_list)
