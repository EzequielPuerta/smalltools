# smalltools
A Python port with a few small tools, snippets and utils (with a lot of WIP) learned in my times as a Smalltalk developer and which I miss a lot.

---
## Behavior:

### 1. SuitableClassFinder:

> Given the hierarchy of an abstract class, it detects the appropriate concrete subclass (deterministically) that satisfies certain attributes obtained as a parameter. Useful for implementing the Strategy design pattern.

#### Example

Let's imagine that we have the following hierarchy:

```python
from abc import ABC

class Vehicle(ABC):
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

class Car(Vehicle):
    def __init__(self, doors_amount, *args):
        self.doors_amount = doors_amount
        super().__init__(*args)

class Bike(Vehicle):
    pass

class Motorkbike(Vehicle):
    pass
```

And we are consuming some silly API. The response could be something like:

```json
vehicles = [
    {'type':'car', 'doors':5, 'motor':1400, 'brand':'renault', 'color':'red'},
    {'type':'bike', 'doors':0, 'motor':0, 'brand':'trek', 'color':'orange'},
    {'type':'motorbike', 'doors':0, 'motor:250, 'brand':'yamaha', 'color':'black'},
    {'type':'car', 'doors':3, 'motor':1200, 'brand':'volkswagen', 'color':'white'},
    ...
]
```

Adding just this snippet to `Vehicle`:

```python
    @classmethod
    def can_handle(cls, vehicle_type):
        return cls.__name__.lower() == vehicle_type
```

...we can get the right subclass for each `json`, just passing the `type` string attribute to the `suitable_for` method:

```python
from smalltools.behavior.suitable_class_finder import SuitableClassFinder

SuitableClassFinder(Vehicle).suitable_for(vehicles[0]['type']) # Returns Car
```

But, what if the API response is not so easy?

```json
vehicles = [
    {'doors':5, 'motor':1400, 'brand':'renault', 'color':'red'},
    {'doors':0, 'motor':0, 'brand':'trek', 'color':'orange'},
    {'doors':0, 'motor:250, 'brand':'yamaha', 'color':'black'},
    {'doors':3, 'motor':1200, 'brand':'volkswagen', 'color':'white'},
    ...
]
```

Don't worry. We can do something like this:

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    @classmethod
    @abstractmethod
    def can_handle(cls, raw_json):
        pass

class Car(Vehicle):
    def __init__(self, doors_amount, *args):
        self.doors_amount = doors_amount
        super().__init__(*args)

    @classmethod
    def can_handle(cls, raw_json):
        return raw_json['doors'] > 0

class Bike(Vehicle):
    @classmethod
    def can_handle(cls, raw_json):
        return raw_json['doors'] == 0 and raw_json['motor'] == 0

class Motorkbike(Vehicle):
    @classmethod
    def can_handle(cls, raw_json):
        return raw_json['doors'] == 0 and raw_json['motor'] > 0
```

Then we have to do the next:

```python
from smalltools.behavior.suitable_class_finder import SuitableClassFinder

SuitableClassFinder(Vehicle).suitable_for(vehicles[0]) # Returns Car
```

Okey, and if you have objects with different "shapes"?

```json
vehicles = [
    {'doors':5, 'motor':1400, 'brand':'renault', 'color':'red'},
    {'brand':'trek', 'color':'orange'},
    {'motor:250, 'brand':'yamaha', 'color':'black'},
    {'doors':3, 'motor':1200, 'brand':'volkswagen', 'color':'white'},
    ...
]
```

---
And thats it! for now...