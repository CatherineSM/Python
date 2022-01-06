#2. Створити клас Person, в якому буде присутнім метод init який буде приймати * аргументів, які зберігатиме в відповідні 
#змінні. Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.

#- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession.

class Person:

    def __init__(self, *args):
        self.name = args[0]
        self.age = args[1]

    def show_age(self):
        print("age:", self.age)

    def print_name(self):
        print("name:", self.name)

    def show_all_information(self):
        for k, v in self.__dict__.items():
            print(k, v, sep=": ")


vasya = Person("Vasya", 20)
petya = Person("Petya", 30)
vasya.profession = "Developer"
petya.profession = "QA engineer"
vasya.show_all_information()

