import math
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n%2==0 or n%3==0:
        return False
    
    for i in range(5, int(n**0.5)+1,6):
        if n%i==0 or n%i+2==0:
            return False
    return True


def first_n_primes(n):
    l = limit(n) + 1
    is_prime = [True] * l
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, l):
        if is_prime[i]:
            for j in range(i*i, l, i):
                is_prime[j]=False

    check = 0
    for i,x in enumerate(is_prime):
        if x:
            print(str(i), end=" ")
            check+=1
            if check==n: break


def limit(n):
    if n<6:return 15
    return int(n * (math.log(n) + math.log(math.log(n))))


if __name__ == "__main__":
    try:
        number = int(input("Enter a number: "))
        # if is_prime(number):
        #     print("prime")
        # else:
        #     print("not prime")
        print(first_n_primes(number))
    except ValueError:
        print("invalid input")