from datetime import datetime


class Book:

    def __init__(self, name, author, year, genre):
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return f"Name: {self.name}; Author: {self.author}; Year: {self.year}; Genre: {self.genre}"


class Student:

    def __init__(self, name, study_class):
        self.name = name
        self.study_class = study_class
        self.books = []

    def __str__(self):
        result = f"Name: {self.name}; Class: {self.study_class}: Books in use: "
        if len(self.books) == 0:
            result += "None"
        else:
            for book in self.books:
                result += f"\n{book}"
        return result


class Library:

    def __init__(self):
        self.books = {}
        self.students = []
        self.action_records = []

    def add_action_record(self, librarian, book, student, action_type):
        action_record = ActionRecord(librarian, book, student, action_type)
        self.action_records.append(action_record)

    def get_book_by_name(self, book_name):
        for book in self.books.keys():
            if book.name == book_name:
                return book
        return None

    def get_student_by_name_and_class(self, student_name, student_class):
        for student in self.students:
            if student.name == student_name and student.study_class == student_class:
                return student
        return None

    def show_books(self):
        print()
        print("Books")
        print("Name".ljust(50), "Author".ljust(30), "Year".ljust(8), "Genre".ljust(15), "Count")
        for book, count in self.books.items():
            print(book.name.ljust(50), book.author.ljust(30), str(book.year).ljust(8), book.genre.ljust(15), count)
        print()

    def show_students(self):
        print()
        print("Students")
        print("Name".ljust(30), "Class".ljust(6))
        for student in self.students:
            print(student.name.ljust(30), student.study_class.ljust(6))
        print()

    def show_action_records(self):
        print()
        print("Action Records")
        print("Librarian".ljust(30) + "Book".ljust(50) + "Student name".ljust(30) + \
              "Student class".ljust(15) + "Action".ljust(15) + "Date and time")

        for action_record in self.action_records:
            print(action_record)

        print()


class Librarian(Library):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def add_book(self, book, count):
        self.books.update({book: count})

    def add_student(self, student):
        self.students.append(student)

    def give_book_to_student(self, book_name, student_name, student_class):
        book = self.get_book_by_name(book_name)
        student = self.get_student_by_name_and_class(student_name, student_class)
        if book and self.books[book] > 0 and student:
            self.books[book] = self.books[book] - 1
            student.books.append(book)
            self.add_action_record(self, book, student, "Give")
            print(f"Book '{book_name}' was successfully given to {student_name} from {student_class}")
        elif not book or self.books[book] == 0:
            print(f"No book '{book_name}' is available in the library")
        elif not student:
            print(f"There is no student {student_name} in {student_class} class")

    def return_book_to_library(self, book_name, student_name, student_class):
        book = self.get_book_by_name(book_name)
        student = self.get_student_by_name_and_class(student_name, student_class)
        if book and student and book in student.books:
            self.books[book] = self.books[book] + 1
            student.books.remove(book)
            self.add_action_record(self, book, student, "Return")
            print(f"Book '{book_name}' was successfully returned by {student_name} from {student_class}")
        elif not book:
            print(f"Book '{book_name}' was not taken from the library")
        elif not student:
            print(f"There is no student {student_name} in {student_class} class")
        elif book not in student.books:
            print(f"Book '{book_name}' was not taken by {student_name} from {student_class}")


class ActionRecord:

    def __init__(self, librarian, book, student, action_type):
        self.librarian = librarian
        self.book = book
        self.student = student
        self.action_type = action_type
        self.time = datetime.now()

    def __str__(self):
        return self.librarian.name.ljust(30) + self.book.name.ljust(50) + self.student.name.ljust(30) + \
               self.student.study_class.ljust(15) + self.action_type.ljust(15) + self.time.strftime("%d.%m.%Y %H:%M:%S")


def init_library():
    librarian = Librarian("Анна Петровна")
    book1 = Book("Война и мир", "Лев Толстой", 1869, "Классика")
    book2 = Book("О новый дивный мир", "Олдос Хаксли", 1932, "Антиутопия")
    book3 = Book("Преступление и наказание", "Федор Достоевский", 1866, "Классика")
    book4 = Book("Властелин Колец", "Джон Толкин", 1954, "Фентези")
    librarian.add_book(book1, 5)
    librarian.add_book(book2, 1)
    librarian.add_book(book3, 2)
    librarian.add_book(book4, 3)
    student1 = Student("Иван Иванов", "9А")
    student2 = Student("Петр Петров", "10Б")
    student3 = Student("Василий Васечкин", "10В")
    librarian.add_student(student1)
    librarian.add_student(student2)
    librarian.add_student(student3)
    return librarian


def start():
    librarian = init_library()
    while True:
        print()
        selected_option = get_option("Choose an option:", ("1. Show books", "2. Show students", "3. Show action records",
                                                           "4. Add book to the library", "5. Add student to the library",
                                                           "6. Give book to student", "7. Return book to the library",
                                                           "8. Exit"))

        if selected_option == 1:
            librarian.show_books()
        elif selected_option == 2:
            librarian.show_students()
        elif selected_option == 3:
            librarian.show_action_records()
        elif selected_option == 4:
            add_new_book(librarian)
        elif selected_option == 5:
            add_new_student(librarian)
        elif selected_option == 6:
            give_book_to_student(librarian)
        elif selected_option == 7:
            return_book_to_the_library(librarian)
        elif selected_option == 8:
            return


def add_new_book(librarian):
    print("Enter the name of the book:")
    book_name = input()
    print("Enter the name of author:")
    author_name = input()
    print("Enter the year of publishing:")
    while True:
        year = input()
        if validate_positive_int(year):
            year = int(year)
            break
        else:
            print("Please, enter the correct year:")
    print("Enter the genre:")
    genre = input()
    book = Book(book_name, author_name, year, genre)
    print("Enter the count:")
    while True:
        count = input()
        if validate_positive_int(count):
            count = int(count)
            break
        else:
            print("Please, enter the correct count:")
    librarian.add_book(book, count)
    print(f"Book {book_name} was successfully added to the library")


def add_new_student(librarian):
    print("Enter the name of the student:")
    student_name = input()
    print("Enter the class of the student:")
    student_class = input()
    student = Student(student_name, student_class)
    librarian.add_student(student)
    print(f"Student {student_name} from {student_class} was successfully added to the library")


def give_book_to_student(librarian):
    print("Enter the name of the book:")
    book_name = input()
    print("Enter the name of the student:")
    student_name = input()
    print("Enter the class of the student:")
    student_class = input()
    librarian.give_book_to_student(book_name, student_name, student_class)


def return_book_to_the_library(librarian):
    print("Enter the name of the book:")
    book_name = input()
    print("Enter the name of the student:")
    student_name = input()
    print("Enter the class of the student:")
    student_class = input()
    librarian.return_book_to_library(book_name, student_name, student_class)


def get_option(title, options=("1. Yes", "2. No")):
    print(title)
    print(*options, sep="\n")
    while True:
        selected_option = input()
        if validate_option(selected_option, len(options)):
            return int(selected_option)
        else:
            print(f"Wrong option. Please, enter a number from 1 to {len(options)}")


def validate_option(input_string, number_of_options):
    try:
        option_number = int(input_string)
        return 1 <= option_number <= number_of_options
    except ValueError as e:
        return False


def validate_positive_int(string):
    try:
        return int(string) > 0
    except ValueError as e:
        return False


start()
