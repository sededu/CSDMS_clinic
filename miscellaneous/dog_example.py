class Dog:

    species = 'canis' # class attribute
    vertebrate = True # class attribute

    def __init__(self, name, age):
        # initializer method
        self.name = name
        self.age = age


maggie = Dog("Maggie", 6)
olive = Dog("Olive", 7)


print(olive.name)
print(olive.age)

