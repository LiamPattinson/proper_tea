"""property_factory

Defines a generic property factory which allows the user to set a transform
and a condition that must be met by any inputs to a property.
"""


def property_factory(
    property_name: str,
    condition=None,
    transform=None,
    condition_err_msg: str = "",
    transform_err_msg: str = "",
):
    """A generic function for creating class properties.

    This function allows the user to assert a condition that must be satisfied
    within the setter, along with the type the property should be set to. It
    does not impose any conditions on the getter.

    Parameters:

        property_name (str): Name of the class property. Must match exactly the
            name assigned, e.g. my_attr = property_factory( "my_attr", ... ).
        condition : Should either be None, meaning any input is accepted, or a
            function taking one argument and returning a bool. An example of a
            common condition may be the property must be non-negative.
        transform : Should either be None, meaning the value is not modified,
            or function that takes one argument. This is used to modify inputs
            to the property. If set to a type (e.g. int, float, str), transform
            will attempt to cast the input to that type.
        condition_err_msg (str): Message to print if 'condition' returns False.
        transform_err_msg (str): Message to print if casting to 'transform'
            fails.

    Returns:

        property : A property decorator. For details on properties, see
            https://realpython.com/python-property/
    """

    def getter(instance):
        """Retrieve the property from the given class instance."""
        return instance.__dict__[property_name]

    def setter(instance, value):
        """Assign 'value' to the property within the given class instance."""

        if condition is not None:
            try:
                valid = condition(value)
            except Exception as e:
                err_msg = (
                    f"Setter condition for property "
                    f"{instance.__class__.__name__}.{property_name} "
                    f"raised exception. See traceback for more info."
                )
                if condition_err_msg:
                    err_msg += f"\n{condition_err_msg}"
                raise ValueError(err_msg) from e

            if not valid:
                err_msg = (
                    f"Setter condition for property "
                    f"{instance.__class__.__name__}.{property_name} "
                    f"returned False."
                )
                if condition_err_msg:
                    err_msg += f"\n{condition_err_msg}"
                raise ValueError(err_msg)

        if transform is not None:
            try:
                value = transform(value)
            except Exception as e:
                err_msg = (
                    f"Setter transform for property "
                    f"{instance.__class__.__name__}.{property_name} "
                    f"raised exception. See traceback for more info."
                )
                if transform_err_msg:
                    err_msg += f"\n{transform_err_msg}"
                raise ValueError(err_msg) from e

        instance.__dict__[property_name] = value

    return property(getter, setter)
