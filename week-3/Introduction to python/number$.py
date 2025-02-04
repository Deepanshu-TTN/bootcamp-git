def to_binary(num):
    if num == 0:
        return "0"
    binary = ""
    while num > 0:
        binary = str(num % 2) + binary
        num //= 2
    return binary

def to_octal(num):
    if num == 0:
        return "0"
    octal = ""
    while num > 0:
        octal = str(num % 8) + octal
        num //= 8
    return octal

def to_hexadecimal(num):
    if num == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    while num > 0:
        hexadecimal = hex_chars[num % 16] + hexadecimal
        num //= 16
    return hexadecimal


num = int(input("Enter a number: "))
print(f"Decimal: {num}")
print(f"Binary: {to_binary(num)}")
print(f"Octal: {to_octal(num)}")
print(f"Hexadecimal: {to_hexadecimal(num)}")
