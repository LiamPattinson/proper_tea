import pytest
import numpy as np
import proper_tea as pt
import proper_tea.numpy


@pytest.fixture
def numpy_array_test_class():
    class MyClass:
        any_array = pt.numpy.numpy_array()
        int_array = pt.numpy.numpy_array(dtype=int)
        float_array = pt.numpy.numpy_array(dtype=float)
        array_1D = pt.numpy.numpy_array(shape=3)
        array_2D = pt.numpy.numpy_array(shape=(2, 3))
        sort_array = pt.numpy.numpy_array(shape=2, dtype=float, sort=True)

    return MyClass()


def test_numpy_array_with_1D_list(numpy_array_test_class):
    test_class = numpy_array_test_class

    test_class.any_array = [1, 2, 3]
    assert isinstance(test_class.any_array, np.ndarray)
    assert test_class.any_array.ndim == 1
    assert np.all(test_class.any_array == [1, 2, 3])


def test_numpy_array_with_2D_list(numpy_array_test_class):
    test_class = numpy_array_test_class

    test_class.any_array = [[1.5, 2.1, 3.6], [4.1, 5.0, 6.9]]
    assert isinstance(test_class.any_array, np.ndarray)
    assert test_class.any_array.dtype == float
    assert test_class.any_array.ndim == 2


def test_numpy_int_array_with_2D_list(numpy_array_test_class):
    test_class = numpy_array_test_class

    test_class.int_array = [[1.5, 2.1, 3.6], [4.1, 5.0, 6.9]]
    assert isinstance(test_class.int_array, np.ndarray)
    assert test_class.int_array.dtype == int
    assert test_class.int_array.ndim == 2
    assert np.all(test_class.int_array == [[1, 2, 3], [4, 5, 6]])


def test_numpy_float_array_with_2D_list(numpy_array_test_class):
    test_class = numpy_array_test_class

    test_class.float_array = [[1, 2, 3], [4, 5, 6]]
    assert isinstance(test_class.float_array, np.ndarray)
    assert test_class.float_array.dtype == float
    assert test_class.float_array.ndim == 2
    assert np.all(test_class.float_array == [[1, 2, 3], [4, 5, 6]])


def test_numpy_array_with_numpy_input(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Set with NumPy arrays
    x = np.linspace(0.0, 100.0, 1001, dtype=np.float16)

    test_class.any_array = x
    assert isinstance(test_class.any_array, np.ndarray)
    assert test_class.any_array.dtype == np.float16
    assert test_class.any_array.ndim == 1
    assert len(test_class.any_array) == 1001
    assert np.all(test_class.any_array == x)
    # It should reference the exact same array in memory
    assert test_class.any_array is x


def test_numpy_int_array_with_numpy_input(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Set with NumPy arrays
    x = np.linspace(0.0, 100.0, 1001, dtype=np.float16)

    test_class.int_array = x
    assert isinstance(test_class.int_array, np.ndarray)
    assert test_class.int_array.dtype == int
    assert test_class.int_array.ndim == 1
    assert len(test_class.int_array) == 1001
    assert np.all(test_class.int_array == np.array(x, dtype=int))
    # It should NOT reference the same array in memory
    assert test_class.int_array is not x


def test_numpy_float_array_with_numpy_input(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Set with NumPy arrays
    x = np.linspace(0.0, 100.0, 1001, dtype=np.float16)

    test_class.float_array = x

    assert isinstance(test_class.float_array, np.ndarray)
    assert test_class.float_array.dtype == float
    assert test_class.float_array.ndim == 1
    assert len(test_class.float_array) == 1001
    assert np.all(np.isclose(test_class.float_array, np.array(x, dtype=float)))
    # It should NOT reference the same array in memory (float != np.float16)
    assert test_class.float_array is not x


def test_numpy_array_with_numpy_input_does_not_copy(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Set with NumPy arrays
    x = np.linspace(0.0, 100.0, 1001)

    # If conversion isn't required, it should not create a copy
    test_class.any_array = x
    assert test_class.any_array is x


def test_fixed_size_numpy_array_1D(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Test it can accept any 3-vector type input
    test_class.array_1D = [1, 2, 3]
    assert len(test_class.array_1D) == 3
    test_class.array_1D = (4.0, 5.0, 6.0)
    assert len(test_class.array_1D) == 3
    test_class.array_1D = np.linspace(1.0, 3.0, 3)
    assert len(test_class.array_1D) == 3

    # Test errors are raised when setting incorrect shape
    with pytest.raises(ValueError) as excinfo:
        test_class.array_1D = [1, 2]
    assert "shape" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        test_class.array_1D = (3,)
    assert "shape" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        test_class.array_1D = np.linspace(1.0, 4.0, 4).reshape((2, 2))
    assert "shape" in str(excinfo.value)
    # should be unchanged after these attempts
    assert len(test_class.array_1D) == 3


def test_fixed_size_numpy_array_2D(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Test it can accept any 3-vector type input
    test_class.array_2D = [[1, 2, 3], [4, 5, 6]]
    assert np.all(np.equal(test_class.array_2D.shape, (2, 3)))
    test_class.array_2D = ((4.0, 5.0, 6.0), (7.0, 8.0, 9.0))
    assert np.all(np.equal(test_class.array_2D.shape, (2, 3)))
    test_class.array_2D = np.linspace(1.0, 6.0, 6).reshape((2, 3))
    assert np.all(np.equal(test_class.array_2D.shape, (2, 3)))

    # Test errors are raised when setting incorrect shape
    with pytest.raises(ValueError) as excinfo:
        test_class.array_2D = [1, 2, 3, 4, 5, 6]
    assert "shape" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        test_class.array_2D = (3,)
    assert "shape" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        test_class.array_2D = np.linspace(1.0, 4.0, 4).reshape((2, 2))
    assert "shape" in str(excinfo.value)
    # should be unchanged after these attempts
    assert np.all(np.equal(test_class.array_2D.shape, (2, 3)))


def test_sorted_numpy_array(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Test it can accept a sorted 2-vector
    test_class.sort_array = [1, 2]
    assert test_class.sort_array[0] == 1
    assert test_class.sort_array[1] == 2

    # Test it automatically sorted an unsorted 2-vector
    test_class.sort_array = [2, 1]
    assert test_class.sort_array[0] == 1
    assert test_class.sort_array[1] == 2
