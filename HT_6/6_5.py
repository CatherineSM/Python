##6. Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї 
#функції.
#   P.S. Повинен вертатись генератор.

def validate_args(args):
    if len(args) < 1:
        raise ValueError("my_range expected at least 1 argument, got 0")
    if len(args) > 3:
        raise ValueError(f"my_range expected at most 3 arguments, got {len(args)}")
    for arg in args:
        if type(arg) is not int:
            raise TypeError(f"'{type(arg).__name__}' object cannot be interpreted as an integer")
    if len(args) == 3 and args[2] == 0:
        raise ValueError("my_range() arg 3 must not be zero")


def my_range(*args):
    validate_args(args)

    if len(args) == 1:
        start, stop, step = 0, args[0], 1
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1
    else:
        start, stop, step = args[0], args[1], args[2]

    if start < stop and step > 0:
        while start < stop:
            yield start
            start += step

    elif start > stop and step < 0:
        while start > stop:
            yield start
            start += step


print("With 1 argument - range from 0 to n exclusive (n > 0):\n", *my_range(10))

print("With 1 argument - range from 0 to n exclusive (n < 0) - empty range:\n", *my_range(-10))

print("With 2 arguments - range from m to n exclusive (m < n):\n", *my_range(5, 10))

print("With 2 arguments - range from m to n exclusive (m > n) - empty range:\n", *my_range(10, 5))

print("With 3 arguments - range from m to n exclusive with step k (m < n, k > 0):\n", *my_range(5, 10, 2))

print("With 3 arguments - range from m to n exclusive with step k (m > n, k < 0):\n", *my_range(10, 5, -2))

print("With 3 arguments - range from m to n exclusive with step k (m < n, k < 0) - empty range:\n", *my_range(5, 10, -2))

print("With 3 arguments - range from m to n exclusive with step k (m > n, k > 0) - empty range\n", *my_range(10, 5, 2))

try:
    print(*my_range())
except ValueError as e:
    print(f"With 0 args - value error:\n{type(e)}: {e}")

try:
    print(*my_range(5, 10, 2, 5))
except ValueError as e:
    print(f"With 4 args - value error:\n{type(e)}: {e}")

try:
    print(*my_range('5', 10))
except TypeError as e:
    print(f"With string arg - type error:\n{type(e)}: {e}")

try:
    print(*my_range(5, 10, 0))
except ValueError as e:
    print(f"With zero step - value error:\n{type(e)}: {e}")
