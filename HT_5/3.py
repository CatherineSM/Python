#3. На основі попередньої функції створити наступний кусок кода:
#   а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь 
#по правилам своєї функції) - як валідні, так і ні;
#   б) створити цикл, який пройдеться по цьому циклу і, користуючись 
#валідатором, перевірить ці дані і надрукує для кожної пари значень відповідне 
#повідомлення, наприклад:
#      Name: vasya
#      Password: wasd
#      Status: password must have at least one digit
#      -----
#      Name: vasya
#      Password: vasyapupkin2000
#      Status: OK
#   P.S. Не забудьте використати блок try/except ;)

class InvalidName(Exception):
	pass

class NumberName(Exception):
	pass

class InvalidPassword(Exception):
	pass

login = input()
password = input()

def is_valid(login, password):
	try:
		if len(login) < 3 or len(login) > 50:
			raise InvalidName
	except InvalidName:
		print("Пароль должен быть от 3 до 50 символов")
	try:
		for i in password:
			if i in "0123456789":
				break
			if i not in "0123456789":
				raise InvalidPassword:
	except InvalidPassword:
		print("В пароле доолжна быть цифра")
	try:
		if len(password) < 8:
			raise InvalidPassword
	except InvalidPassword:
		print("В пароле меньше 8 символов")
	try:
		for j in login:
			if j in "0123456789":
				raise NumberName
	except NumberName:
		print("В имени не должно быть цифр")
    return "ОК"

user_list = [["kate", "1wefcwefw"], ["tanya", "slds32"], ["maryna1", "1wceesdcerfrefsd"]]

for datas in user_list:
	login = datas[0]
	password = datas[1]
	print ("Имя: ", login)
	print ("Пароль ", password)
	print (is_valid(login, password))
