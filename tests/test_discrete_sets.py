import proper_tea as pt
import pytest

@pytest.fixture
def in_set_test_class():
    class MyClass:
        alphabet = pt.in_set({'A','B','C'})
        numbers = pt.in_set({1,2,3})
        strings = pt.in_set({'foo','bar'})
    return MyClass()


def test_in_set(in_set_test_class):
    # Try setting each where we expect it to work
    in_set_test_class.alphabet = 'A'
    assert in_set_test_class.alphabet == 'A'
    in_set_test_class.alphabet = 'B'
    assert in_set_test_class.alphabet == 'B'
    in_set_test_class.alphabet = 'C'
    assert in_set_test_class.alphabet == 'C'
    in_set_test_class.numbers = 1
    assert in_set_test_class.numbers == 1
    assert isinstance(in_set_test_class.numbers, int)
    in_set_test_class.numbers = 2
    assert in_set_test_class.numbers == 2
    assert isinstance(in_set_test_class.numbers, int)
    in_set_test_class.numbers = 3
    assert in_set_test_class.numbers == 3
    assert isinstance(in_set_test_class.numbers, int)
    in_set_test_class.numbers = 1.0
    assert in_set_test_class.numbers == 1
    assert isinstance(in_set_test_class.numbers, float)
    in_set_test_class.numbers = 2.0
    assert in_set_test_class.numbers == 2
    assert isinstance(in_set_test_class.numbers, float)
    in_set_test_class.numbers = 3.0
    assert in_set_test_class.numbers == 3
    assert isinstance(in_set_test_class.numbers, float)
    in_set_test_class.strings = 'foo'
    assert in_set_test_class.strings == 'foo'
    assert isinstance(in_set_test_class.strings, str)
    in_set_test_class.strings = 'bar'
    assert in_set_test_class.strings == 'bar'
    assert isinstance(in_set_test_class.strings, str)
    # Test a variety of failure cases
    alphabet_fail_cases = ['D', 'hello world', 5, 'a', None]
    for fail_case in alphabet_fail_cases:
        with pytest.raises(ValueError) as excinfo:
            in_set_test_class.alphabet = fail_case
    numbers_fail_cases = [ 4, 'hello world', '1', None]
    for fail_case in numbers_fail_cases:
        with pytest.raises(ValueError) as excinfo:
            in_set_test_class.numbers = fail_case
    strings_fail_cases = [ 'f', 'Foo', 5, None]
    for fail_case in strings_fail_cases:
        with pytest.raises(ValueError) as excinfo:
            in_set_test_class.strings = fail_case

