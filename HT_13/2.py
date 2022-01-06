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

