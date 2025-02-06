evens = open('even.txt', 'a')
odds = open('odd.txt', 'a')
floats = open('floats.txt', 'a')

with open('numbers.txt', "r") as num_file:
    for num in num_file:
        match float(num)%2:
            case 1:
                odds.write(num)
            case 0:
                evens.write(num)
            case _:
                floats.write(num)

odds.close()
evens.close()
floats.close()
