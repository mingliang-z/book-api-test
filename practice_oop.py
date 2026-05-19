



class Calculator:
    def __init__(self):
        self.result = 0

    def add(self,n):
        self.result += n
        return self.result

    def subtract(self,n):
        self.result -= n
        return self.result

    def multiply(self,n):
        self.result *= n
        return self.result

    def reset(self):
        self.result = 0
        return self.result



# calc = Calculator()
# calc.add(5)
# print(calc.result)
# calc.subtract(3)
# print(calc.result)
# calc.multiply(3)
# print(calc.result)
# calc.reset()
# print(calc.result)

calc = Calculator()
# calc.add(5).subtract(3).multiply(3).reset()
# print(calc.result)

# calc.add(5).subtract(3)
# print(calc.result)

calc1 = calc.add(6)
print(calc1)
calc2 = calc.subtract(calc1)
print(calc2)