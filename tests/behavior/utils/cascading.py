import operator
from smalltools_st.behavior.cascading import cascading
from typing import Callable, Any


class BasicCounter():

    def __init__(self, start_value: int) -> None:
        self.current_value = start_value

    def __str__(self) -> str:
        return str(self.current_value)

    def __repr__(self) -> str:
        return repr(self.current_value)

    def __calculate(self, operation: Callable[[Any, Any], Any], number: int) -> int:
        return operation(self.current_value, number)

    def increment(self) -> None:
        self.current_value = self.__calculate(operator.add, 1)

    def decrement(self) -> None:
        self.current_value = self.__calculate(operator.sub, 1)

@cascading
class Counter():

    def __init__(self, start_value: int) -> None:
        self.current_value = start_value

    def __str__(self) -> str:
        return str(self.current_value)

    def __repr__(self) -> str:
        return repr(self.current_value)

    def __calculate(self, operation: Callable[[Any, Any], Any], number: int) -> int:
        return operation(self.current_value, number)

    def add(self, number: int) -> None:
        self.current_value = self.__calculate(operator.add, number)

    def subtract(self, number: int) -> None:
        self.current_value = self.__calculate(operator.sub, number)

    def multiply(self, number: int) -> None:
        self.current_value = self.__calculate(operator.mul, number)

    def divide(self, number: int) -> None:
        self.current_value = self.__calculate(operator.truediv, number)

    def is_even(self) -> bool:
        return True if self.current_value % 2 == 0 else False

@cascading
class Repository():

    def __init__(self, start_values: list) -> None:
        self.content = start_values

    def __str__(self) -> str:
        display = ''
        for key, value in self.content.items():
            display = display + f'* {key} : {value}\n'
        return display

    def __repr__(self) -> str:
        return str(self)

    def add(self, key: Any, value: Any) -> None:
        self.content[key] = value

    def remove(self, key: Any) -> None:
        del self.content[key]

    def look_for(self, key: Any) -> Any:
        return self.content[key]
