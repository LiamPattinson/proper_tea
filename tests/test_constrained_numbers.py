from proper_tea import positive_int, positive_float, in_range

import pytest

@pytest.fixture
def property_class():
    class MyClass:

        pos_float = positive_float()
        pos_int = positive_int()
        ranged = in_range((-1.0,1.0))

        def __init__(self):
            self.pos_float = 1.0
            self.pos_int = 5
            self.ranged = 0.0

    return MyClass()

def test_positive_float(property_class):
    # Ensure that the user can assign to a positive_float
    property_class.pos_float = 7.2
    assert property_class.pos_float == 7.2
    # Zero should be allowed
    property_class.pos_float = 0.0
    assert property_class.pos_float == 0.0
    # Ensure that the user cannot set a positive_float property to a negative
    with pytest.raises(ValueError) as execinfo:
        property_class.pos_float = -1.0
    assert "False" in str(execinfo.value)
    # Ensure the value is unchanged by a failed assignment
    assert property_class.pos_float == 0.0
    # Ensure that the user cannot set a non-floatable
    with pytest.raises(ValueError) as execinfo:
        property_class.pos_float = "hello world"
    assert "raise" in str(execinfo.value)
    # Ensure the value is unchanged by a failed assignment
    assert property_class.pos_float == 0.0

def test_positive_int(property_class):
    # Ensure that the user can assign to a positive_int
    property_class.pos_int = 7
    assert property_class.pos_int == 7
    # Zero should be allowed
    property_class.pos_int = 0
    assert property_class.pos_int == 0
    # floats should be cast to ints correctly
    property_class.pos_int = 5.2
    assert property_class.pos_int == 5
    # Ensure that the user cannot set to something negative
    with pytest.raises(ValueError) as execinfo:
        property_class.pos_int = -3
    assert "False" in str(execinfo.value)
    # Ensure the value is unchanged by a failed assignment
    assert property_class.pos_int == 5
    # Ensure that the user cannot set to something that can't be cast to int
    with pytest.raises(ValueError) as execinfo:
        property_class.pos_int = "hello world"
    assert "raise" in str(execinfo.value)
    # Ensure the value is unchanged by a failed assignment
    assert property_class.pos_int == 5

def test_in_range(property_class):
    # Ensure that the user can assign to a in_range
    property_class.ranged = 0.5
    assert property_class.ranged == 0.5
    # The edge values should be allowed
    property_class.ranged = 1.0
    assert property_class.ranged == 1.0
    property_class.ranged = -1.0
    assert property_class.ranged == -1.0
    # No type restrictions, should be able to set to int
    property_class.ranged = 1
    assert property_class.ranged == 1
    assert isinstance( property_class.ranged, int)
    # Ensure that the user cannot set to something larger than upper bound
    with pytest.raises(ValueError) as execinfo:
        property_class.ranged = 1.5
    assert "False" in str(execinfo.value)
    # Ensure that the user cannot set to something smaller than lower bound
    with pytest.raises(ValueError) as execinfo:
        property_class.ranged = -1.1
    assert "False" in str(execinfo.value)
    # Ensure the value is unchanged by a failed assignment
    assert property_class.ranged == 1
    # Ensure that the user cannot set to something that can't be compared
    with pytest.raises(ValueError) as execinfo:
        property_class.ranged = "hello world"
    assert "raise" in str(execinfo.value)
    # Ensure the value is unchanged by a failed assignment
    assert property_class.ranged == 1
