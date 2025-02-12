class MathOperations:
    def add(*args):
        # s=0
        # for n in args:
        #     s+=n
        # return s
        match len(args):
            case 2:
                return args[0]+args[1]
            case 3: 
                return args[0]+args[1]+args[2]
            case _:
                raise ValueError("add() method only accepts 2 or 3 values")

m = MathOperations

print(m.add(2,3,5))
print(m.add(2,3))