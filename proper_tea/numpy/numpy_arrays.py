"""numpy_arrays

Defines specialised property_factory's that convert inputs to numpy arrays. Numpy is
not a dependency of proper_tea, so users must have installed numpy separately in
order for these features to work.
"""

from ..property_factory import property_factory
import numpy as np


def numpy_array(shape=None, dtype=None, sort: bool = False):
    """Creates property that converts to numpy array.

    Uses np.asarray, so does not copy when passed a valid array.

    Parameters:

        shape: Optionally require a given shape.
        dtype: Optionally require the property to convert to given datatype.
        sort: Optionally sort any input arrays

    Returns:

        property
    """
    # if a single int is given as shape, convert to 1-tuple
    if isinstance(shape, int):
        shape = (shape,)

    def condition(x):
        if shape is not None:
            # Ensure shape of x is same as that provided by user
            return np.all(np.equal(np.shape(x), shape))
        # If shape is None, don't perform checks
        return True

    condition_err_msg = f"Must have shape {shape}"

    asarray = lambda x: np.asarray(x, dtype=dtype)
    if sort:
        transform = lambda x: np.sort(asarray(x))
    else:
        transform = asarray

    transform_err_msg = "Must be convertable to NumPy array"
    if dtype is not None:
        transform_err_msg += f" with datatype {dtype.__name__}"

    return property_factory(
        condition=condition,
        condition_err_msg=condition_err_msg,
        transform=transform,
        transform_err_msg=transform_err_msg,
    )
