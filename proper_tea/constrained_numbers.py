"""constrained_numbers

Defines specialised property_factory's for adding constraints on numbers such
as ints and floats. The properties can enforce type, require values are within
a given range, are greater than 0, etc.
"""

from .property_factory import property_factory

def positive(property_name: str, no_zero: bool=False, type_constraint=None):
    """Creates property that must be positive, possibly including zero

    Parameters:

        property_name (str): Name of the class property. Must match exactly the
            name assigned, e.g. my_attr = positive( "my_attr", ... ).
        no_zero (bool): If set to true, excludes zero as a possibility.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """
    if no_zero:
        condition=lambda x: x > 0
        condition_err_msg="Must be greater than 0"
    else:
        condition=lambda x: x >= 0
        condition_err_msg="Must be greater than or equal to 0"

    if type_constraint is not None:
        transform_err_msg = f"Must be convertable to {type_constraint.__name__}"
    else:
        transform_err_msg = ""

    return property_factory(
        property_name,
        condition=condition,
        condition_err_msg=condition_err_msg,
        transform=type_constraint,
        transform_err_msg=transform_err_msg,
    )

def positive_float(property_name: str, no_zero: bool = False):
    """Creates property that must be positive float"""
    return positive(property_name,no_zero=no_zero,type_constraint=float)

def positive_int(property_name: str, no_zero: bool = False):
    """Creates property that must be positive int"""
    return positive(property_name,no_zero=no_zero,type_constraint=int)

def in_range(property_name: str, bounds):
    """Creates property that must be between bounds[0] and bounds[1]."""
    return property_factory(
        property_name,
        condition=lambda x: x >= bounds[0] and x <= bounds[1],
        condition_err_msg=(
            f"Must be within the range [{bounds[0]},{bounds[1]}] (inclusive)"
        ),
    )
