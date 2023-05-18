### 1. cascading

> Given a class, this decorator takes all its methods that do not return `None` and returns `self` instead. Otherwise, keeps the original value. This behavior is similar to the Smalltalk's one. If a method does not return an explicit value, it just returns `self`.

Let's see this useless class:

```python
import operator

class Counter():
    def __init__(self, start_value):
        self.current_value = start_value

    def __calculate(self, operation, number):
        return operation(self.current_value, number)

    def add(self, number):
        self.current_value = self.__calculate(operator.add, number)

    def subtract(self, number):
        self.current_value = self.__calculate(operator.sub, number)
```

If you want to use that you can write something like this:

```python
my_counter = Counter(0)     #  0
my_counter.add(10)          # 10
my_counter.add(5)           # 15
my_counter.subtract(4)      # 11
my_counter.current_value    # 11
```

I don't like it. It's too verbose and there is a lot of repeated code. I would like to write something like this:

```python
my_counter = Counter(0)\    #  0
    .add(10)\               # 10
    .add(5)\                # 15
    .subtract(4)\           # 11
my_counter.current_value    # 11

# or...

Counter(0)\                 #  0
    .add(10)\               # 10
    .add(5)\                # 15
    .subtract(4)\           # 11
    .current_value          # 11
```

So we can change our class a little bit to achieve this. Just lets add `return self` to `add` and `subtract`. (oops! [Guido van Rossum will be upset with me](https://mail.python.org/pipermail/python-dev/2003-October/038855.html)... Sorry Guido, let me have some fun)

```python
import operator

class Counter():
    def __init__(self, start_value):
        self.current_value = start_value

    def __calculate(self, operation, number):
        return operation(self.current_value, number)

    def add(self, number):
        self.current_value = self.__calculate(operator.add, number)
        return self

    def subtract(self, number):
        self.current_value = self.__calculate(operator.sub, number)
        return self
```

But... if we have a lot of methods like `add` that we would like to use in a "cascade" way but we don't want to return `self` on each one? Introducing @cascading:

```python
import operator
from smalltools_st.behavior.cascading import cascading

@cascading
class Counter():
    def __init__(self, start_value):
        self.current_value = start_value

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
```

TaDa!

```python
Counter(0).add(10).add(5).subtract(4).current_value     # 11
```

The decorator "understands" that all methods which returns `None` should return `self` instead, so you don't have to return it explicitly. The `__calculate` method keeps returning the math result because its different than `None`. For the sake of transparency lets see the next example:

```python
import operator
from smalltools_st.behavior.cascading import cascading

@cascading
class Counter():
    ...
    # all the same stuff
    ...
    def is_even(self):
        return True if self.current_value % 2 == 0 else False

Counter(0).add(10).subtract(4).multiply(2).divide(3).is_even()  # True
```

#### Notes

> But... what about if you really want to return an explicit `None` value? 
Well, just don't do that... next question!
...🦗...🦗...🦗...
It's not enough for you? Are you asking why?
Okey, read [this](https://en.wikipedia.org/wiki/Null_object_pattern) about the [Null Object refactoring](https://en.wikipedia.org/wiki/Null_object_pattern).

#### The `Cascade` class

Now, lets talk about what is happening under the hood. As surely you already know, decorators in Python are common methods indeed. In our case, `@cascading` is a method that takes a class, defines a new one called `Decorator` and replaces the first with it. In honor of its name, it [decores](https://en.wikipedia.org/wiki/Decorator_pattern) the passed class allowing the mentioned behavior.

To achieve this, `Decorator` uses another class: `Cascade`. This one is interesting because you can use it too, especially when you want a *cascade-like* behavior on a built-in class:

```python
from smalltools_st.behavior.cascading import Cascade

# Idk if it's useful, but... here we go
Cascade([]).append(1).append(2).append(3).yourself                      # [1,2,3]
Cascade({}).update({1:1}).update({2:2}).update({3:3}).yourself          # {1:1, 2:2, 3:3}
Cascade(True).__or__(False).__and__(True).yourself                      # True
Cascade(0).__add__(10).__sub__(4).__mul__(2).__truediv__(3).yourself    # 4.0
Cascade('').__add__('  hello world!  ').strip().capitalize().yourself   # 'Hello world!'
```

Or with a class from another package or something like that:

```python
import operator
from smalltools_st.behavior.cascading import Cascade

# Let's suppose that you don't have ownership over 
# this class. For example it could be on another 
# package, so you cann't put the @cascading on it.
class BasicCounter():

    def __init__(self, start_value):
        self.current_value = start_value

    def __calculate(self, operation, number):
        return operation(self.current_value, number)

    def increment(self):
        self.current_value = self.__calculate(operator.add, 1)

    def decrement(self):
        self.current_value = self.__calculate(operator.sub, 1)

# This could be a bit more useful
Cascade(BasicCounter(0))\
    .increment()\
    .decrement()\
    .increment()\
    .increment()\
    .current_value  # 2
```



---

[< Back](/README.md)