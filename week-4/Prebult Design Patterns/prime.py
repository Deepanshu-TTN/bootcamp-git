class Prime:
    def __init__(self,prime=2,n=0,m=0):
        self.N=n
        self.M=m
        self.prime = prime


    def _is_prime(self, n):
        if n<=1:
            return False
        if n<=3:
            return True
        if n%2==0 or n%3==0:
            return False
        for i in range(5, int(n**0.5)+1, 6):
            if n%i==0 or n%i+1==0:
                return False
        return True
    

    def generate_prime(self, start=1):
        num = start+1
        while True:
            if self._is_prime(num):
                yield num
            num+=1


    def primes_less_than(self):
        for num in range(self.N, 2, -1):
            if self._is_prime(num):
                yield num


    def primes_between(self):
        out = []
        for num in range(self.N, self.M + 1):
            if self._is_prime(num):
                out.append(num)
        return out


    def __add__(self, next_rank):
        for _ in range(next_rank):
            next_prime = self.generate_prime(self.prime)
        return next_prime
    

    def __iadd__(self):
        for _ in range(self.prime):
            next_prime = self.generate_prime(self.prime)
        self.prime = next_prime
        return self.prime


    def __len__(self):
        return sum(1 for _ in self.primes_between(self.N, self.M))
    

'''
Checking the functionality of _is_prime() function
P_object = Prime()
print(P_object._is_prime(9))
print(P_object._is_prime(13))
'''


'''
Generate Prime greater than N
P_object = Prime(n=20)
primes_generator = P_object.generate_prime(start=P_object.N)
for i in range(10):
    print(next(primes_generator))
'''


'''
Generate Prime numbers less than N
P_object = Prime(n=20)
primes_generator = P_object.primes_less_than()
for i in range(10):
    try:
        print(next(primes_generator))
    except StopIteration:
        print('No more primes to generate!')
        break
'''