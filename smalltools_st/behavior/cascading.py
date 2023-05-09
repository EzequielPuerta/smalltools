import numbers
from abc import ABC, abstractmethod
from smalltools_st.behavior.suitable_class_finder import SuitableClassFinder


try:
    callable
except NameError:
    # Python 3.0 and 3.1 does not include this built-in function
    def callable(obj):
        return hasattr(type(obj), '__call__')


class ReplaceStrategy(ABC):

    def __init__(self, cascade):
        self.cascade = cascade

    @classmethod
    @abstractmethod
    def targets(cls):
        pass

    @classmethod
    def can_handle(cls, target):
        return any(map(lambda _class: isinstance(target, _class), cls.targets()))

    @abstractmethod
    def replace(self, new_content):
        pass

    @abstractmethod
    def result(self, value):
        pass


class Replace(ReplaceStrategy):

    @classmethod
    def targets(cls):
        return (bool, numbers.Number, str)

    def replace(self, new_content):
        self.cascade.yourself = new_content

    def result(self, value):
        return self.cascade


class NoReplace(ReplaceStrategy):

    @classmethod
    def targets(cls):
        return (list, dict)

    def replace(self, new_content):
        pass

    def result(self, value):
        return self.cascade if value is None else value


class Cascade():

    def __init__(self, content, always=False, replace_strategy=None):
        self.yourself = content
        self.always = always
        self.strategy = (replace_strategy if replace_strategy is not None else \
            SuitableClassFinder(ReplaceStrategy).suitable_for(content, default_subclass=NoReplace))(self)

    def __repr__(self):
        return repr(self.yourself)

    def __getattr__(self, method_name):
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


def cascading(original_class):
    class Decorator():
        def __init__(self, *args, **kwargs):
            self.wrapped = Cascade(original_class(*args, **kwargs))

        def __str__(self):
            return str(self.wrapped)

        def __repr__(self):
            return repr(self.wrapped)

        def __getattr__(self, method_name):
            attr = getattr(self.wrapped, method_name)
            if callable(attr):
                def adapt(*args, **kwargs):
                    result = attr(*args, **kwargs)
                    return self if isinstance(result, Cascade) else result
                return adapt
            else:
                return attr
    return Decorator
