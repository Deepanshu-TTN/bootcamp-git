# x,y = 2, 0
# print(x/y)


#program to record user vote

class AgeException(Exception):
    def __init__(self, message, error):
        super().__init__(message)
        self.message = message
        self.error = error

    def __str__(self):
        return f"{self.message} (Error Code: {self.error})"

try:
    age = int(input("Age? "))
    if age < 18:
        raise AgeException("You can't vote", 294)
    vote = input("Vote for? ")

except AgeException as e:
    print(str(e))