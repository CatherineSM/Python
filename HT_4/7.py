#7. Написати функцію, яка приймає на вхід список і підраховує кількість 
#однакових елементів у ньому.

array = [3, 3, 2, 7, 8, 1, 1, 4, 1]

def counter(array):
    array_d = {}.fromkeys(array, 0)
    for a in array:
        array_d[a] += 1
    return  array_d
   
print(counter(array))
