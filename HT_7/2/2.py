#2. Написати функцію, яка приймає два параметри: ім'я файлу та кількість 
#символів.
#На екран повинен вивестись список із трьома блоками - символи з початку, із 
#середини та з кінця файлу.
#Кількість символів в блоках - та, яка введена в другому параметрі.
#Придумайте самі, як обробляти помилку, наприклад, коли кількість символів 
#більша, ніж є в файлі (наприклад, файл із двох символів і треба вивести по 
#одному символу, то що виводити на місці середнього блоку символів?)
#В репозиторій додайте і ті файли, по яким робили тести.
#Як визначати середину файлу (з якої брать необхідні символи) - кількість 
#символів поділити навпіл, а отримане "вікно" символів відцентрувати щодо 
#середини файла і взяти необхідну кількість. В разі необхідності заокруглення 
#одного чи обох параметрів - дивіться на свій розсуд.
#Наприклад:
#█ █ █ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ ░ █ █ █    - правильно
#                     ⏫ центр
#█ █ █ ░ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ █ █ █    - неправильно
#                     ⏫ центр
import math

user_file = input("Введите название тектового файла")+'.txt'
user_number = int(input("Введите количество символов в блоке"))

def blocks(user_file, user_number):
   with open(user_file, encoding ='utf-8') as file:
      file_list = list(file.read())
      file_len = len(file_list)
      if user_number > file_len:
         raise ValueError("В файле недостаточно символов")
      elif user_number <= 0:  
         raise ValueError("Количество символов в блоке должно быть плюсовым")
      elif file_len == 2 and user_number == 1:
         block1 = file_list[0]
         block3 = 'Недостаточно символов для выведения третьего блока'
         blok2 = file_list[-1]
      elif file_len == 2 and user_number == 1:
         block1 = file_list[2]
         block3 = 'Недостаточно символов для выведения третьего блока'
         blok2 = file_list[-2]         
      elif file_len == 1:
         block1 = file_list
         block3 = 'Недостаточно символов для выведения третьего блока'
         blok2 = 'Недостаточно символов для выведения второго блока'
      elif file_len == user_number:
         block1 = 'Блоки идентичны', file_list
         return  block1
      else:
            block1 = file_list[:user_number]
            block3 = file_list[-user_number: len(file_list)]
            center = math.ceil(len(file_list)/2)
            blok2 = file_list[center - math.ceil(user_number/2): center + math.floor(user_number/2)]  
   return  block1, blok2, block3

print(blocks(user_file, user_number))
      
