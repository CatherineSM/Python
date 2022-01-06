#Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки(включіть фантазію).

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

    def add_book(self, book, count):
        self.books.update({book: count})

    def give_book_to_student(self, book, student):
        if book in self.books.keys() and self.books[book] > 0:
            self.books[book] = self.books[book] - 1
            student.books.append(book)
        else:
            print(f"No book {book.name} is available in the library")

    def return_book_to_library(self, book, student):
        if book in self.books.keys():
            self.books[book] = self.books[book] + 1
            student.books.remove(book)
        else:
            print(f"The book {book.name} was not taken from the library")

    def __str__(self):
        result = "Library:\n"
        for book, count in self.books.items():
            result += f"Book: {book}; Count: {count};"
        return result


book = Book("Война и мир", "Лев Толстой", 1869, "Классика")
student = Student("Петя", "10А")
library = Library()
library.add_book(book, 5)
print("\nInitial state:\n")
print(library)
print(student)

library.give_book_to_student(book, student)
print("\nAfter student took book from the library:\n")
print(library)
print(student)

library.return_book_to_library(book, student)
print("\nAfter student returned book to the library:\n")
print(library)
print(student)