class Dog:
    """
    Dog(name, age) returns an instance of the Dog class.
    """

    species = 'canis' # class attribute
    vertebrate = True # class attribute

    def __init__(self, name, age):
        # initializer method
        self.name = name
        self.age = age

    def bark(self):
        """
        writes out woof to console
        """
        print("woof")







maggie = Dog(name="Maggie", age=6)
olive = Dog("Olive", 7)


print(olive.name)
print(olive.age)

print(maggie)
print(maggie.name)
print(maggie.bark)
maggie.bark()

help(maggie)

