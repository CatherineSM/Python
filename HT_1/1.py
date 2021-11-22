#1 .Write a script which accepts a sequence of comma-separated numbers from user and generate a list and a tuple with those numbers.
#Sample data : 1, 5, 7, 23
#Output :
#List : [‘1', ' 5', ' 7', ' 23']
#Tuple : (‘1', ' 5', ' 7', ' 23')


values = input()
list = values.split(",")
tuple = tuple(list)
print('List : ',list)
print('Tuple : ',tuple)