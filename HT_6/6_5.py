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
