class Dumbclass:

    def __init__(self, x):
        self.y = x
        self.z = 2

    def __str__(self):
        return str(self.y)+str(self.z)

    def foo(self, y):
        self.y += y
        self.z = y*self.y

    def garble(self, other):
        self.z = other.y

a = Dumbclass(2)
b = Dumbclass(3)
a.foo(9)
print(a)
b.garble(a)
print(b)
b.foo(4)
print(b)
