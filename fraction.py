class Fraction:
    """ that represents a fraction consisting of a numerator and a denominator. 
    """
    def __init__(self, numerator, denominator):
        """initialize numerator and denominator"""
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        """returns a string representation of the fraction"""
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        """returns a string representation of the fraction"""
        return f"{self.numerator}/{self.denominator}"
   
    def __add__(self, other):
        """returns the sum of two fractions"""
        numerator = self.numerator * other.denominator + self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __sub__(self, other):
        """subtract"""
        numerator = self.numerator * other.denominator - self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __mul__(self, other):
        """multiply"""
        numerator = self.numerator * other.denominator * self.denominator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __truediv__(self, other):
        """divide"""
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)
print(Fraction(3, -60))
