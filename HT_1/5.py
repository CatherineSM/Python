#5. Write a script to convert decimal to hexadecimal
#Sample decimal number: 30, 4
#Expected output: 1e, 04

def toHex(decimal):
    hex_str = ''
    digits = "0123456789ABCDEF"
    if decimal == 0:
       return '0'

    while decimal != 0:
        hex_str += digits[decimal % 16]
        decimal = decimal // 16

    return hex_str[::-1]

numbers = [30, 4]
print([toHex(x) for x in numbers])
