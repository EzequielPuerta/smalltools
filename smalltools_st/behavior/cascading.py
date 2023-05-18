import numbers
from abc import ABC, abstractmethod
from smalltools_st.behavior.suitable_class_finder import SuitableClassFinder
from typing import Tuple, Union


class ReplaceStrategy(ABC):
    """It models the replacement behavior of a Cascade instance"""

    def __init__(self, cascade: "Cascade") -> None:
        self.cascade = cascade

    @classmethod
    @abstractmethod
    def possible_classes(cls) -> Tuple[type]:
        """Tuple with classes that work well with this replacement strategy"""

    @classmethod
    def can_handle(cls, target: object) -> bool:
        """Returns a bool answer about if 'target' is instance of any 'possible_classes'"""
        return any(map(lambda _class: isinstance(target, _class), cls.possible_classes()))

    @abstractmethod
    def replace(self, new_content: object) -> None:
        """Replaces the related Cascade's value according to the replacement strategy"""

    @abstractmethod
    def result(self, value: object) -> object:
        """Returns the new value of the Cascade according to the replacement strategy"""


class Replace(ReplaceStrategy):
    """Replacement strategy for immutable classes"""

    @classmethod
    def possible_classes(cls) -> Tuple[type]:
        return (bool, numbers.Number, str, tuple)

    def replace(self, new_content: object) -> None:
        self.cascade.yourself = new_content

    def result(self, value: object) -> object:
        return self.cascade


class NoReplace(ReplaceStrategy):
    """Replacement strategy for mutable classes"""

    @classmethod
    def possible_classes(cls) -> Tuple[type]:
        return (list, dict, set)

    def replace(self, new_content: object) -> None:
        pass

    def result(self, value: object) -> object:
        return self.cascade if value is None else value


class Cascade():
    """Given an object, it allows you to evaluate multiple consecutive
    methods in a cascade-like format. It is also knows as 'method chaining',
    'fluent interface', etc."""

    def __init__(self, content: object, always: bool = False, replace_strategy: Union[None, ReplaceStrategy] = None):
        self.yourself = content
        self.always = always
        self.strategy = (replace_strategy if replace_strategy is not None else
            SuitableClassFinder(ReplaceStrategy).suitable_for(content, default_subclass=NoReplace))(self)

    def __str__(self) -> str:
        return str(self.yourself)

    def __repr__(self) -> str:
        return repr(self.yourself)

    def __getattr__(self, method_name: str) -> object:
        attr = getattr(self.yourself, method_name)
        if callable(attr):
            def myself(*args, **kwargs):
                value = attr(*args, **kwargs)
                self.strategy.replace(value)
                if not self.always:
                    return self.strategy.result(value)
                else:
                    return self
            return myself
        else:
            return attr


def cascading(original_class: type) -> type:
    """Decorating a custom class with it, you could use it as a Cascade object."""
    class Decorator():
        def __init__(self, *args, **kwargs):
            self.wrapped = Cascade(original_class(*args, **kwargs))

        def __str__(self) -> str:
            return str(self.wrapped)

        def __repr__(self) -> str:
            return repr(self.wrapped)

        def __getattr__(self, method_name: str) -> object:
            attr = getattr(self.wrapped, method_name)
            if callable(attr):
                def adapt(*args, **kwargs):
                    result = attr(*args, **kwargs)
                    return self if isinstance(result, Cascade) else result
                return adapt
            else:
                return attr
    return Decorator
