#6. Write a script to check whether a specified value is contained in a group of values.
#Test Data :
#3 -> [1, 5, 8, 3] : True
#-1 -> (1, 5, 8, 3) : False

input_number = int(input())
list_number =   [1, 5, 8 , 3]
if input_number in list_number:
    print('True')
else:
    print('False')