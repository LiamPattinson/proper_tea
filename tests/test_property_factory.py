from proper_tea import property_factory

import pytest

@pytest.fixture
def property_class():
    class MyClass:
        ends_in_dot = property_factory(
            "ends_in_dot",
            transform=lambda z: z + ".",
            transform_err_msg="Couldn't add to end of string",
        )

        equal_to_5 = property_factory(
            "equal_to_5",
            condition=lambda z: z == 5,
            condition_err_msg="Should be equal to 5",
        )

        less_than_5 = property_factory(
            "less_than_5",
            condition=lambda z: z < 5,
            condition_err_msg="Should be less than 5",
        )

        def __init__(self):
            self.ends_in_dot = "string"
            self.equal_to_5 = 5
            self.less_than_5 = 3

    return MyClass()

def test_property_factory_transform(property_class):
    # MyClass.ends_in_dot should always have '.' in the last place
    assert property_class.ends_in_dot[-1] == "."
    # Test reassigning repeats the transform
    property_class.ends_in_dot = "hello world"
    assert property_class.ends_in_dot == "hello world."
    # Test that it can happen recusively
    property_class.ends_in_dot = property_class.ends_in_dot
    assert property_class.ends_in_dot == "hello world.."
    # Test that it raises ValueError when passed a non string
    with pytest.raises(ValueError) as execinfo:
        property_class.ends_in_dot = 17
    assert "raise" in str(execinfo.value)
    # Ensure that a failed set doesn't modify
    assert property_class.ends_in_dot == "hello world.."

def test_property_factory_condition(property_class):
    # MyClass.equal_to_5 should fail when given anything except 5
    # Note that it should not raise an exception in the vast
    # majority of cases.
    assert property_class.equal_to_5 == 5
    assert isinstance(property_class.equal_to_5, int)
    # Test it works for floats
    property_class.equal_to_5 = 5.0
    assert property_class.equal_to_5 == 5.0
    assert isinstance(property_class.equal_to_5, float)
    # Test it returns false when given something else
    with pytest.raises(ValueError) as execinfo:
        property_class.equal_to_5 = 0
    assert "False" in str(execinfo.value)
    # Ensure that a failed set didn't change the result
    assert property_class.equal_to_5 == 5.0
    # MyClass.less_than_5 should instead raise an exception
    # if given a string. First test that it works:
    property_class.less_than_5 = 3
    assert property_class.less_than_5 == 3
    # Now try giving it a string
    with pytest.raises(ValueError) as execinfo:
        property_class.less_than_5 = "hello world."
    assert "raise" in str(execinfo.value)
