import operator
from smalltools_st.behavior.cascading import cascading


class BasicCounter():

    def __init__(self, start_value):
        self.current_value = start_value

    def __str__(self):
        return str(self.current_value)

    def __repr__(self):
        return repr(self.current_value)

    def __calculate(self, operation, number):
        return operation(self.current_value, number)

    def increment(self):
        self.current_value = self.__calculate(operator.add, 1)

    def decrement(self):
        self.current_value = self.__calculate(operator.sub, 1)

@cascading
class Counter():

    def __init__(self, start_value):
        self.current_value = start_value

    def __str__(self):
        return str(self.current_value)

    def __repr__(self):
        return repr(self.current_value)

    def __calculate(self, operation, number):
        return operation(self.current_value, number)

    def add(self, number):
        self.current_value = self.__calculate(operator.add, number)

    def subtract(self, number):
        self.current_value = self.__calculate(operator.sub, number)

    def multiply(self, number):
        self.current_value = self.__calculate(operator.mul, number)

    def divide(self, number):
        self.current_value = self.__calculate(operator.truediv, number)

    def is_even(self):
        return True if self.current_value % 2 == 0 else False

@cascading
class Repository():

    def __init__(self, start_values):
        self.content = start_values

    def __str__(self):
        display = ''
        for key, value in self.content.items():
            display = display + f'* {key} : {value}\n'
        return display

    def __repr__(self):
        return str(self)

    def add(self, key, value):
        self.content[key] = value

    def remove(self, key):
        del self.content[key]

    def look_for(self, key):
        return self.content[key]
