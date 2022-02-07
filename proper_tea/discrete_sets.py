"""discrete_sets

Defines specialised property_factory's that require properties may only be within a 
user-defined set.
"""

from .property_factory import property_factory


def in_set(discrete_set):
    """Creates property that must take its value from a given set

    Parameters:

        discrete_set (Iterable): Defines the set of values that the property may take.

    Returs:

        property
    """
    condition = lambda x: x in set(discrete_set)
    condition_err_msg = f"Must be one of {set(discrete_set)}"
    return property_factory(
        condition=condition,
        condition_err_msg=condition_err_msg,
    )
