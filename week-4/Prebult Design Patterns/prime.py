class Prime:
    '''
    Prime class\n
    an object can be initialized by giving an optional prime number\n
    and optional N and M number for operations\n
    '''
    def __init__(self,prime=2,n=0,m=0):
        self.N = n
        self.M = m
        self.prime = prime


    def _is_prime(self, n):
        '''
        Check if the given number is Prime or not.\n
        Takes a number as an argument\n
        Returns True or False\n
        '''
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n%2 == 0 or n%3 == 0:
            return False
        for i in range(5, int(n**0.5) + 1, 6):
            if n%i == 0 or n%i+1 == 0:
                return False
        return True
    

    def generate_prime(self, start=1):
        '''
        This is a generator function that generates prime numbers\n
        Takes an optional starting value as an argument\n
        Yields an integer\n
        '''
        num = start + 1
        while True:
            if self._is_prime(num):
                yield num
            num += 1


    def primes_less_than(self):
        '''
        Generator function to generate prime numbers less than N attribute of the instance
        '''
        for num in range(self.N, 2, -1):
            if self._is_prime(num):
                yield num


    def primes_between(self):
        '''Returns a list of prime numbers between N and M attribute of an intance'''
        out = []
        for num in range(self.N, self.M + 1):
            if self._is_prime(num):
                out.append(num)
        return out


    def __repr__(self):
        '''returns representation of the instance, a number'''
        return str(self.prime)


    def __str__(self):
        '''returns string literal for the instance'''
        return str(self.prime)


    def __add__(self, next_rank):
        '''function that dictates the logic behind add operation'''
        add_generator = self.generate_prime(self.prime)
        for _ in range(next_rank):
            next_prime = next(add_generator)
        return next_prime
    

    def __iadd__(self, next_rank):
        '''function does the add operation and updates the instance's current prime attribute'''
        next_prime = self.__add__(next_rank)
        self.prime = next_prime
        return self.prime


    def __len__(self):
        '''function that returns number of prime numbers between N and M parameters of the instace'''
        return sum(1 for _ in self.primes_between())
    

    

'''
Checking the functionality of _is_prime() function
P_object = Prime()
print(P_object._is_prime(9))
print(P_object._is_prime(13))
'''


'''
Generate Prime greater than N
'''
P_object = Prime(n=20)
primes_generator = P_object.generate_prime(start=P_object.N)
for i in range(10):
    print(next(primes_generator))


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


'''
Generate primes between N and M and len gives the number of primes between those
P_object = Prime(n=2, m=50)
print(P_object.primes_between())
print(len(P_object))
'''


'''
Check add iadd str and repr methods 
p = Prime(3)
print(p)
print(p+1)
print(p+2)
p+=3
print(p)
'''