'''
File structure:
    package
        |__ subpackage1
            |__ module1.py
            |__ module2.py
            |__ __init__.py

        |__ subpackage2
            |__ module3.py 
            |__ __init__.py
        
        |__ __init__.py
'''

#we are inside module3.py

#absolute path import
# from package.subpackage1.module1 import funs
# funs()

#relative path import
from ..subpackage1.module2 import ABC

def func():
    abc = ABC()
    print(dir(abc))