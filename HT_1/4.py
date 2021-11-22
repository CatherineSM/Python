#Write a script to concatenate N strings

number = int(input())
result = ''
for step in range(number):
    user_input = input()
    result = result + user_input
print(result)