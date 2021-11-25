#4. Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна 
#повертати якийсь результат. Також створiть четверу ф-цiю, яка в тiлi викликає
# 3 попереднi, обробляє повернутий ними результат та також повертає результат.
# Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3

def SumNumbers(n):
    summ = 0 
    n2 = n
    while n>0:
        t = n%10 
        summ += t
        n = n//10 
    print("Сумма чисел ", n2, " = ", summ)
    return summ

def MulNumbers(n):
    summ = n % 100
    n2 = n
    while n>0:
        t = n%10 
        summ *= t
        n = n//10 
    print("Произведение чисел ", n2, " = ", summ)
    return summ

def MaxDigit(n):
    maxD = 0
    n2 = n
    while n>0:
        t = n%10
        if t>maxD:
            maxD = t
        n = n//10
    print("Максимальное число ", n2, " = ", maxD)
    return maxD

def OperationNumber(n, fn1, fn2, fn3):
    fn1(n) 
    fn2(n) 
    fn3(n)

OperationNumber(2736, MaxDigit, SumNumbers, MulNumbers)