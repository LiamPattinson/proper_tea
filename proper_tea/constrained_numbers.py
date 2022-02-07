"""constrained_numbers

Defines specialised property_factory's for adding constraints on numbers such
as ints and floats. The properties can enforce type, require values are within
a given range, are greater than 0, etc.

Contains:
    - floating_point
    - integer
    - positive
    - positive_float
    - positive_int
    - negative
    - negative_float
    - negative_int
    - greater_than
    - int_greater_than
    - float_greater_than
    - less_than
    - int_less_than
    - float_less_than
    - in_range
    - float_in_range
    - int_in_range
    - not_in_range
    - float_not_in_range
    - int_not_in_range
"""

from .property_factory import property_factory

# Define helper functions


def _convert_args(type_constraint=None):
    if type_constraint is None:
        return {}
    return {
        "transform": type_constraint,
        "transform_err_msg": f"Must be convertible to {type_constraint.__name__}",
    }


def _greater_than_args(x, inclusive: bool):
    return {
        "condition": (lambda y: y >= x if inclusive else y > x),
        "condition_err_msg": (
            f"Must be greater than {'or equal to ' if inclusive else ''}{x}"
        ),
    }


def _less_than_args(x, inclusive: bool):
    return {
        "condition": (lambda y: y <= x if inclusive else y < x),
        "condition_err_msg": (
            f"Must be less than {'or equal to ' if inclusive else ''}{x}"
        ),
    }


def _test_bounds(bounds):
    try:
        if len(bounds) != 2:
            raise ValueError("bounds should have len() == 2")
        if bounds[0] >= bounds[1]:
            raise ValueError("bounds[0] must be less than bounds[1]")
    except TypeError as e:
        err_msg = "bounds should be a subscriptable object with len() == 2"
        raise TypeError(err_msg) from e
    return bounds


def _ranged_inclusive_as_tuple(inclusive):
    ranged_err = (
        "When specifying if a range is inclusive, users should supply "
        "either a single bool or an subscriptable object with len()==2"
    )
    if isinstance(inclusive, bool):
        inclusive = (inclusive, inclusive)
    try:
        if len(inclusive) != 2:
            raise ValueError(ranged_err)
        inclusive[0]
        inclusive[1]
    except TypeError as e:
        raise TypeError(ranged_err) from e
    return tuple(inclusive)


def _in_range_args(bounds, inclusive: True):
    inclusive = _ranged_inclusive_as_tuple(inclusive)

    def condition(x):
        above_min = x >= bounds[0] if inclusive[0] else x > bounds[0]
        below_max = x <= bounds[1] if inclusive[1] else x < bounds[1]
        return above_min and below_max

    err_msg = (
        f"Must be within range {'[' if inclusive[0] else '('}{bounds[0]},"
        f"{bounds[1]}{']' if inclusive[1] else ')'}"
    )
    return {"condition": condition, "condition_err_msg": err_msg}


def _not_in_range_args(bounds, inclusive: False):
    inclusive = _ranged_inclusive_as_tuple(inclusive)

    def condition(x):
        below_min = x <= bounds[0] if inclusive[0] else x < bounds[0]
        above_max = x >= bounds[1] if inclusive[1] else x > bounds[1]
        return below_min or above_max

    err_msg = (
        f"Must be outside range {'[' if inclusive[0] else '('}{bounds[0]},"
        f"{bounds[1]}{']' if inclusive[1] else ')'}"
    )
    return {"condition": condition, "condition_err_msg": err_msg}


# Define properties


def floating_point():
    """Creates property that transforms to floating point"""
    return property_factory(**_convert_args(float))


def integer():
    """Creates property that transforms to int"""
    return property_factory(**_convert_args(int))


def boolean():
    """Creates property that transforms to bool"""
    return property_factory(**_convert_args(bool))


def positive(allow_zero: bool = True, type_constraint=None):
    """Creates property that must be positive, possibly including zero

    Parameters:

        allow_zero (bool): If set to False, excludes zero as a possibility.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """

    return property_factory(
        **_greater_than_args(0, inclusive=allow_zero),
        **_convert_args(type_constraint),
    )


def positive_float(allow_zero: bool = True):
    """Creates property that must be positive float

    Parameters:

        allow_zero (bool): If set to False, excludes zero as a possibility.

    Returns:

        property
    """
    return positive(allow_zero=allow_zero, type_constraint=float)


def positive_int(allow_zero: bool = True):
    """Creates property that must be positive int

    Parameters:

        allow_zero (bool): If set to False, excludes zero as a possibility.

    Returns:

        property
    """
    return positive(allow_zero=allow_zero, type_constraint=int)


def negative(allow_zero: bool = False, type_constraint=None):
    """Creates property that must be negative, possibly including zero

    Parameters:

        allow_zero (bool): If set to True, includes zero as a possibility.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """
    return property_factory(
        **_less_than_args(0, inclusive=allow_zero),
        **_convert_args(type_constraint),
    )


def negative_float(allow_zero: bool = True):
    """Creates property that must be negative float

    Parameters:

        allow_zero (bool): If set to True, includes zero as a possibility.

    Returns:

        property
    """
    return negative(allow_zero=allow_zero, type_constraint=float)


def negative_int(allow_zero: bool = True):
    """Creates property that must be negative int

    Parameters:

        allow_zero (bool): If set to True, includes zero as a possibility.

    Returns:

        property
    """
    return negative(allow_zero=allow_zero, type_constraint=int)


def greater_than(x, inclusive: bool = False, type_constraint=None):
    """Creates property that must be greater than (or equal to) some value

    Parameters:

        x: Value that the property must be greater than
        inclusive (bool): If set to True, includes x as a possibility.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """

    return property_factory(
        **_greater_than_args(x, inclusive=inclusive),
        **_convert_args(type_constraint),
    )


def float_greater_than(x, inclusive: bool = False):
    """Creates property that must be a float greater than (or equal to)
    some value

    Parameters:

        x: Value that the property must be greater than
        inclusive (bool): If set to True, includes x as a possibility.

    Returns:

        property
    """
    return greater_than(x, inclusive=inclusive, type_constraint=float)


def int_greater_than(x, inclusive: bool = False):
    """Creates property that must be an int greater than (or equal to)
    some value

    Parameters:

        x: Value that the property must be greater than
        inclusive (bool): If set to True, includes x as a possibility.

    Returns:

        property
    """
    return greater_than(x, inclusive=inclusive, type_constraint=int)


def less_than(x, inclusive: bool = False, type_constraint=None):
    """Creates property that must be less than (or equal to) some value

    Parameters:

        x: Value that the property must be less than
        inclusive (bool): If set to True, includes x as a possibility.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """

    return property_factory(
        **_less_than_args(x, inclusive=inclusive),
        **_convert_args(type_constraint),
    )


def float_less_than(x, inclusive: bool = False):
    """Creates property that must be a float less than (or equal to)
    some value

    Parameters:

        x: Value that the property must be less than
        inclusive (bool): If set to True, includes x as a possibility.

    Returns:

        property
    """
    return less_than(x, inclusive=inclusive, type_constraint=float)


def int_less_than(x, inclusive: bool = False):
    """Creates property that must be an int less than (or equal to)
    some value

    Parameters:

        x: Value that the property must be less than
        inclusive (bool): If set to True, includes x as a possibility.

    Returns:

        property
    """
    return less_than(x, inclusive=inclusive, type_constraint=int)


def in_range(bounds, inclusive=True, type_constraint=None):
    """Creates property that must be between bounds[0] and bounds[1].

    Parameters:

        bounds: Subscriptable with len()==2, where bounds[0] is the lower
            bound and bounds[1] is the upper bound.
            Requires bounds[1] > bounds[0].
        inclusive (bool): If set to False, values falling on the upper and
            lower bounds will not be accepted. Can set one bound to be
            inclusive and the other exclusive by setting this to a tuple
            of 2 bools, e.g. (True,False) makes the lower bound inclusive
            while the upper bound is not.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """
    return property_factory(
        **_in_range_args(bounds, inclusive),
        **_convert_args(type_constraint),
    )


def float_in_range(bounds, inclusive=True):
    """Creates property that must be a float between bounds[0] and bounds[1].

    Parameters:

        bounds: Subscriptable with len()==2, where bounds[0] is the lower
            bound and bounds[1] is the upper bound.
            Requires bounds[1] > bounds[0].
        inclusive (bool): If set to False, values falling on the upper and
            lower bounds will not be accepted. Can set one bound to be
            inclusive and the other exclusive by setting this to a tuple
            of 2 bools, e.g. (True,False) makes the lower bound inclusive
            while the upper bound is not.

    Returns:

        property
    """
    return in_range(bounds, inclusive, type_constraint=float)


def int_in_range(bounds, inclusive=True):
    """Creates property that must be an int between bounds[0] and bounds[1].

    Parameters:

        bounds: Subscriptable with len()==2, where bounds[0] is the lower
            bound and bounds[1] is the upper bound.
            Requires bounds[1] > bounds[0].
        inclusive (bool): If set to False, values falling on the upper and
            lower bounds will not be accepted. Can set one bound to be
            inclusive and the other exclusive by setting this to a tuple
            of 2 bools, e.g. (True,False) makes the lower bound inclusive
            while the upper bound is not.

    Returns:

        property
    """
    return in_range(bounds, inclusive, type_constraint=int)


def not_in_range(bounds, inclusive=False, type_constraint=None):
    """Creates property that must be outside bounds[0] and bounds[1].

    Parameters:

        bounds: Subscriptable with len()==2, where bounds[0] is the lower
            bound and bounds[1] is the upper bound.
            Requires bounds[1] > bounds[0].
        inclusive (bool): If set to False, values falling on the upper and
            lower bounds will not be accepted. Can set one bound to be
            inclusive and the other exclusive by setting this to a tuple
            of 2 bools, e.g. (True,False) makes the lower bound inclusive
            while the upper bound is not.
        type_constraint: If set to None, does not constrain. Can be set to int,
            float, etc to enforce the underlying type of the property.

    Returns:

        property
    """
    return property_factory(
        **_not_in_range_args(bounds, inclusive),
        **_convert_args(type_constraint),
    )


def float_not_in_range(bounds, inclusive=False):
    """Creates property that must be a float outside bounds[0] and bounds[1].

    Parameters:

        bounds: Subscriptable with len()==2, where bounds[0] is the lower
            bound and bounds[1] is the upper bound.
            Requires bounds[1] > bounds[0].
        inclusive (bool): If set to False, values falling on the upper and
            lower bounds will not be accepted. Can set one bound to be
            inclusive and the other exclusive by setting this to a tuple
            of 2 bools, e.g. (True,False) makes the lower bound inclusive
            while the upper bound is not.

    Returns:

        property
    """
    return not_in_range(bounds, inclusive, type_constraint=float)


def int_not_in_range(bounds, inclusive=False):
    """Creates property that must be an int outside bounds[0] and bounds[1].

    Parameters:

        bounds: Subscriptable with len()==2, where bounds[0] is the lower
            bound and bounds[1] is the upper bound.
            Requires bounds[1] > bounds[0].
        inclusive (bool): If set to False, values falling on the upper and
            lower bounds will not be accepted. Can set one bound to be
            inclusive and the other exclusive by setting this to a tuple
            of 2 bools, e.g. (True,False) makes the lower bound inclusive
            while the upper bound is not.

    Returns:

        property
    """
    return not_in_range(bounds, inclusive, type_constraint=int)
