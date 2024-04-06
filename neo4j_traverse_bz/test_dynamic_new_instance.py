
#python3动态创建实例演示
class Apple:pass

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def get_info(self) -> str:
        return f"Name: {self.name}, Age: {self.age}"

instance=Person.__new__(Person)
instance.__init__("xx",44)
print(instance.get_info())

import typing
typ:typing.Type[Person|Apple]=Person
instance2=typ.__new__(typ)
instance2.__init__("gh",33)
print(instance2.get_info())
