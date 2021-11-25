#6. Маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pij
#np46ij7k5j78p3kj546p465jnpoj35po6j345" -> просто потицяв по клавi
#   Створіть ф-цiю, яка буде отримувати рядки на зразок цього, яка оброблює 
#наступні випадки:
#-  якщо довжина рядка в діапазонi 30-50 -> прiнтує довжину, кiлькiсть букв та 
#цифр
#-  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр (
#лише з буквами)
#-  якщо довжина бульше 50 - > ваша фантазiя

user_string = input()

symbols = len(user_string)
user_line = list(user_string)
symbols = len(user_string)
count_numbers = 0
#total #current #ch #i,s

def countinng(symbols):
    if symbols < 30:
        def counting(user_string):
            total, current = 0, ''
            for ch in user_string:
                if ch.isdigit():
                    current += ch
                elif current!='':
                    total += int(current)
                    current = ''
            if current != '':
                total += int(current)
            return total
        result = counting(user_string)
        return result  
    elif symbols < 51:        
        res = [len(list(filter(f,user_line))) for f in (str.isalpha,str.isdigit)]
        return len(user_string), res
    elif symbols > 50:
        return "Код и так большой незачем пихать сюда что-то еще))) "

result = countinng(symbols)
print(result)

#Кусочек кода для объедененных символов никак не могу вписать в основной код(((( 
#symbols_total = ''
#for symbol in user_string:
#    if not symbol.isdigit():
#        symbols_total = symbols_total + symbol
