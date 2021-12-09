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
      file_len = len(file.read())
      center = math.ceil(file_len / 2)
   if file_len < user_number*3:
      raise ValueError("В файле недостаточно символов")
   elif user_number <= 0:
      raise ValueError("Количество символов в блоке должно быть плюсовым")
   else:
      with open(user_file, encoding ='utf-8') as file:
         file_block1 = file.read(user_number)
         file_block2_2 = file.read(center - math.ceil(user_number * 1.5))
         file_block2 = file.read(user_number)
         if user_number % 2 == 0:
            file_block2_2 = file.read(center - math.floor(user_number * 2))
         else:   
            file_block2_2 = file.read(center - math.floor(user_number * 1.5))
         file_block3 = file.read(user_number)
   return center, file_block1, file_block2, file_block3

print(blocks(user_file, user_number))
      