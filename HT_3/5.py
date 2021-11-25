#5. Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями;
#-  Створiть просту умовну конструкцiю(звiсно вона повинна бути в тiлi ф-цiї), 
#пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" і при 
#нерiвностi змiнних "х" та "у" вiдповiдь повертали рiзницю чисел.
#-  Повиннi опрацювати такi умови:
#-  x > y;       вiдповiдь - х бiльше нiж у на z
#-  x < y;       вiдповiдь - у бiльше нiж х на z
#-  x == y.      вiдповiдь - х дорiвнює z

def compare(x, y):
    if x == y:
        return 'х дорiвнює z'
    elif x < y:
        return 'у бiльше нiж х на', y - x
    elif x > y:
        return 'х бiльше нiж у на', x - y 

x = int(input())
y = int(input())
result = compare(x, y)
print(" ".join(map(str,result)))