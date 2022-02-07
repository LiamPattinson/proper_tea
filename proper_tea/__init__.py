try:
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("proper_tea")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]

from .property_factory import property_factory
from .constrained_numbers import (
    floating_point,
    integer,
    boolean,
    positive,
    positive_int,
    positive_float,
    negative,
    negative_int,
    negative_float,
    greater_than,
    int_greater_than,
    float_greater_than,
    less_than,
    int_less_than,
    float_less_than,
    in_range,
    int_in_range,
    float_in_range,
    not_in_range,
    int_not_in_range,
    float_not_in_range,
)
from .discrete_sets import in_set
