from package.subpackage1.module2 import ABC
abc = ABC()
print(dir(abc))
print(abc._protected)
print(abc.__private)