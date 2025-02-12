class Database:
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.loc = "/.dbsqlite3"

    def some_method(self, *args, **kwargs):
        pass

db1 = Database()
db2 = Database()
print(f'db1 {db1}')
print(f'db2 {db2}')
print(db1 is db2)