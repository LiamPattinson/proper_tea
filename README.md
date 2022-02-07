# proper_tea

A Python package for automating the creation of common class properties.

## Usage

Properties are a useful feature of modern Python, allowing users to cleanly add 'getter' and 'setter' functions in an unobtrusive manner. For example, a common use case is to ensure a class attribute cannot be set to a negative number:

```python
class Item:

    def __init__(self,weight):
        self.weight = weight # weight in kg

    @property
    def weight(self):
        # A simple getter
        return self._weight
    
    @weight.setter
    def weight(self, value):
        # Cannot set negative weight!
        if value < 0:
            raise ValueError("Weight cannot be negative")
        self._weight = value

item = Item(2.4)
# The 'getter' function is called when accessing the 'weight' attribute
assert item.weight == 2.4
# The 'setter' function is called when assigning to the 'weight' attribute
item.weight = 4.6
assert item.weight == 4.6
# The following raises an exception
# item.weight = -1.0
```

A downside of properties is that they require a significant amount of boilerplate code. Each property will usually require the implementation of two functions, and often this code is repeated. For example, if the Item class above were also given a 'price' attribute, it too cannot be negative, so the user must implement near-identical getter and setter functions.

`proper_tea` makes use of 'property factories', inspired by the book Fluent Python (Luciano Ramalho, O'Reilly, 2015), to automate the creation of common properties. Using `proper_tea`, the above class may instead be written:

```python
import proper_tea as pt

class Item:
    
    weight = pt.positive() # weight in kg

    def __init__(self,weight):
        self.weight = weight
```

Extending it to include other variables couldn't be easier:

```python
import proper_tea as pt

class Item:
    
    weight = pt.positive() # weight in kg
    price = pt.positive_int() # price in pennies
    temperature = pt.float_greater_than(-273.15) # temperature in Celsius
    rating = pt.int_in_range((1,10)) # 1-10 star rating
    format = pt.in_set({ "jpeg", "png"}) # output format, must match strings exactly

    def __init__(self, weight, price, temperature, rating, format):
        self.weight = weight
        self.price = price
        self.temperature = temperature
        self.rating = rating
        self.format = format
```

## Installation

The latest version of `proper_tea` may be installed using pip:

`python3 -m pip install proper_tea`

To install from the GitHub repo, first clone it, and then install via:

`python3 -m pip install .`

To run the tests:

```
python3 -m pip install .[tests]
pytest tests
```

## Additional Features

### NumPy support

`proper_tea` provides property factories for NumPy arrays:

```python
import numpy as np
import proper_tea as pt
import proper_tea.numpy

class MyClass:

    x = pt.numpy.numpy_array()
    
    def __init__(self, x):
        self.x = x

# Automatically convert iterables to NumPy array
my_class = MyClass([1,2,3])
assert isinstance( my_class.x, np.ndarray)

# Assigning to my_class.x will also automatically convert
my_class.x = [[4,5,6],[7,8,9]]
assert isinstance( my_class.x, np.ndarray)
assert my_class.x.ndim == 2

# Existing NumPy arrays are not copied
y = np.linspace( 0.0, 100.0, 1001)
my_class.x = y
assert x is y
```
