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

    return MyClass()

def test_numpy_array(numpy_array_test_class):
    test_class = numpy_array_test_class

    # Set with lists
    test_class.any_array = [1,2,3]
    assert isinstance( test_class.any_array, np.ndarray)
    assert test_class.any_array.ndim == 1
    assert np.all(test_class.any_array == [1,2,3])

    test_class.int_array = [[1.5,2.1,3.6],[4.1,5.0,6.9]]
    assert isinstance( test_class.int_array, np.ndarray)
    assert test_class.int_array.dtype == int
    assert test_class.int_array.ndim == 2
    assert np.all( test_class.int_array == [[1,2,3],[4,5,6]])

    test_class.float_array = [[1,2,3],[4,5,6]]
    assert isinstance( test_class.float_array, np.ndarray)
    assert test_class.float_array.dtype == float
    assert test_class.float_array.ndim == 2
    assert np.all( test_class.float_array == [[1,2,3],[4,5,6]])

    # Set with NumPy arrays
    x = np.linspace(0.,100.,1001,dtype=np.float16)

    test_class.any_array = x
    assert isinstance( test_class.any_array, np.ndarray)
    assert test_class.any_array.dtype == np.float16
    assert test_class.any_array.ndim == 1
    assert len(test_class.any_array) == 1001
    assert np.all(test_class.any_array == x)
    # It should reference the exact same array in memory
    assert test_class.any_array is x

    test_class.int_array = x
    assert isinstance( test_class.int_array, np.ndarray)
    assert test_class.int_array.dtype == int
    assert test_class.int_array.ndim == 1
    assert len(test_class.int_array) == 1001
    assert np.all(test_class.int_array == np.array(x,dtype=int))
    # It should NOT reference the same array in memory
    assert test_class.int_array is not x

    test_class.float_array = x
    assert isinstance( test_class.float_array, np.ndarray)
    assert test_class.float_array.dtype == float
    assert test_class.float_array.ndim == 1
    assert len(test_class.float_array) == 1001
    assert np.all(np.isclose(test_class.float_array,np.array(x,dtype=float)))
    # It should NOT reference the same array in memory (float != np.float16)
    assert test_class.float_array is not x
    # However, it should work if we instead reference a NumPy array with type 'float'
    y = np.linspace(0.,100.,1001,dtype=float)
    test_class.float_array = y
    assert test_class.float_array is y 

