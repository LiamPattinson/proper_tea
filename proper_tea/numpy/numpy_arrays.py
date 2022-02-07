"""numpy_arrays

Defines specialised property_factory's that convert inputs to numpy arrays. Numpy is
not a dependency of proper_tea, so users must have installed numpy separately in
order for these features to work.
"""

from ..property_factory import property_factory
import numpy as np


def numpy_array(dtype=None):
    """Creates property that converts to numpy array.

    Uses np.asarray, so does not copy when passed a valid array.

    Parameters:

        dtype: Optionally require the property to convert to given datatype.

    Returns:

        property
    """
    transform = lambda x: np.asarray(x, dtype=dtype)
    transform_err_msg = "Must be convertable to NumPy array"
    if dtype is not None:
        transform_err_msg += f" with datatype {dtype.__name__}"
    return property_factory(
        transform=transform,
        transform_err_msg=transform_err_msg,
    )
