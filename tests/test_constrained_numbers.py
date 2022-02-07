import proper_tea as pt
import pytest
from itertools import product


@pytest.fixture
def basic_test():
    class MyClass:
        floating_point = pt.floating_point()
        integer = pt.integer()
        boolean = pt.boolean()

    return MyClass()


class TestBasics:
    def test_floating_point(self, basic_test):
        # Ensure the user can assign
        basic_test.floating_point = 81.3
        assert basic_test.floating_point == 81.3
        assert isinstance(basic_test.floating_point, float)
        # Ensure that they can set using int, but it remains a float
        basic_test.floating_point = 60
        assert basic_test.floating_point == 60
        assert isinstance(basic_test.floating_point, float)
        # Ensure it won't allow something that won't convert
        with pytest.raises(ValueError) as excinfo:
            basic_test.floating_point = "hello world"
        assert "convert" in str(excinfo.value)

    def test_integer(self, basic_test):
        # Ensure the user can assign
        basic_test.boolean = True
        assert basic_test.boolean
        assert isinstance(basic_test.boolean, bool)
        basic_test.boolean = False
        assert not basic_test.boolean
        assert isinstance(basic_test.boolean, bool)
        # Anything should work, in theory
        basic_test.boolean = 60.5
        assert basic_test.boolean
        assert isinstance(basic_test.integer, bool)
        basic_test.boolean = 0.0
        assert not basic_test.boolean
        assert isinstance(basic_test.integer, bool)
        basic_test.boolean = "hello world"
        assert basic_test.boolean
        assert isinstance(basic_test.integer, bool)
        basic_test.boolean = []
        assert not basic_test.boolean
        assert isinstance(basic_test.integer, bool)
        basic_test.boolean = None
        assert not basic_test.boolean
        assert isinstance(basic_test.integer, bool)

    def test_integer(self, basic_test):
        # Ensure the user can assign
        basic_test.integer = 27
        assert basic_test.integer == 27
        assert isinstance(basic_test.integer, int)
        # Ensure that they can set using float, but it rounds to int
        basic_test.integer = 60.5
        assert basic_test.integer == 60
        assert isinstance(basic_test.integer, int)
        # Ensure it won't allow something that won't convert
        with pytest.raises(ValueError) as excinfo:
            basic_test.integer = "hello world"
        assert "convert" in str(excinfo.value)


@pytest.fixture
def pos_neg_test(allow_zero: bool):
    class MyClass:

        pos = pt.positive(allow_zero=allow_zero)
        pos_float = pt.positive_float(allow_zero=allow_zero)
        pos_int = pt.positive_int(allow_zero=allow_zero)
        neg = pt.negative(allow_zero=allow_zero)
        neg_float = pt.negative_float(allow_zero=allow_zero)
        neg_int = pt.negative_int(allow_zero=allow_zero)

        def __init__(self):
            self.allow_zero = allow_zero

    return MyClass()


class TestPosNeg:
    @pytest.mark.parametrize("allow_zero", [False, True])
    def test_positive(self, pos_neg_test):
        # Ensure the user can assign any positive
        pos_neg_test.pos = 4
        assert pos_neg_test.pos == 4
        assert isinstance(pos_neg_test.pos, int)
        pos_neg_test.pos = 4.5
        assert pos_neg_test.pos == 4.5
        assert isinstance(pos_neg_test.pos, float)
        # Ensure negatives fail
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos = -4
        assert "greater than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos = -4.5
        assert "greater than" in str(excinfo.value)
        # Ensure 0 works if allow_zero is true
        if pos_neg_test.allow_zero:
            pos_neg_test.pos = 0
            assert pos_neg_test.pos == 0
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.pos = -4.5
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.pos = 0
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos = "hello world"

    @pytest.mark.parametrize("allow_zero", [False, True])
    def test_positive_float(self, pos_neg_test):
        # Ensure the user can assign any positive float
        pos_neg_test.pos_float = 4.5
        assert pos_neg_test.pos_float == 4.5
        assert isinstance(pos_neg_test.pos_float, float)
        # Ensure ints are converted
        pos_neg_test.pos_float = 4
        assert pos_neg_test.pos_float == 4
        assert isinstance(pos_neg_test.pos_float, float)
        # Ensure negatives fail
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos_float = -4.5
        assert "greater than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos_float = -4
        assert "greater than" in str(excinfo.value)
        # Ensure 0 works if allow_zero is true
        if pos_neg_test.allow_zero:
            pos_neg_test.pos_float = 0
            assert pos_neg_test.pos_float == 0
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.pos_float = -4.5
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.pos_float = 0
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos_float = "hello world"

    @pytest.mark.parametrize("allow_zero", [False, True])
    def test_positive_int(self, pos_neg_test):
        # Ensure the user can assign any positive int
        pos_neg_test.pos_int = 4
        assert pos_neg_test.pos_int == 4
        assert isinstance(pos_neg_test.pos_int, int)
        # Ensure floats are converted
        pos_neg_test.pos_int = 4.4
        assert pos_neg_test.pos_int == 4
        assert isinstance(pos_neg_test.pos_int, int)
        # Ensure negatives fail
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos_int = -4
        assert "greater than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos_int = -4.5
        assert "greater than" in str(excinfo.value)
        # Ensure 0 works if allow_zero is true
        if pos_neg_test.allow_zero:
            pos_neg_test.pos_int = 0
            assert pos_neg_test.pos_int == 0
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.pos_int = -4
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.pos_int = 0
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.pos_int = "hello world"

    @pytest.mark.parametrize("allow_zero", [False, True])
    def test_negative(self, pos_neg_test):
        # Ensure the user can assign any negative
        pos_neg_test.neg = -4
        assert pos_neg_test.neg == -4
        assert isinstance(pos_neg_test.neg, int)
        pos_neg_test.neg = -4.5
        assert pos_neg_test.neg == -4.5
        assert isinstance(pos_neg_test.neg, float)
        # Ensure positives fail
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg = 4
        assert "less than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg = 4.5
        assert "less than" in str(excinfo.value)
        # Ensure 0 works if allow_zero is true
        if pos_neg_test.allow_zero:
            pos_neg_test.neg = 0
            assert pos_neg_test.neg == 0
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.neg = 4.5
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.neg = 0
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg = "hello world"

    @pytest.mark.parametrize("allow_zero", [False, True])
    def test_negative_float(self, pos_neg_test):
        # Ensure the user can assign any negative float
        pos_neg_test.neg_float = -4.5
        assert pos_neg_test.neg_float == -4.5
        assert isinstance(pos_neg_test.neg_float, float)
        # Ensure ints are converted
        pos_neg_test.neg_float = -4
        assert pos_neg_test.neg_float == -4
        assert isinstance(pos_neg_test.neg_float, float)
        # Ensure positives fail
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg_float = 4.5
        assert "less than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg_float = 4
        assert "less than" in str(excinfo.value)
        # Ensure 0 works if allow_zero is true
        if pos_neg_test.allow_zero:
            pos_neg_test.neg_float = 0
            assert pos_neg_test.neg_float == 0
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.neg_float = 4.5
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.neg_float = 0
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg_float = "hello world"

    @pytest.mark.parametrize("allow_zero", [False, True])
    def test_negative_int(self, pos_neg_test):
        # Ensure the user can assign any negative int
        pos_neg_test.neg_int = -4
        assert pos_neg_test.neg_int == -4
        assert isinstance(pos_neg_test.neg_int, int)
        # Ensure floats are converted (should round up)
        pos_neg_test.neg_int = -4.4
        assert pos_neg_test.neg_int == -4
        assert isinstance(pos_neg_test.neg_int, int)
        # Ensure positives fail
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg_int = 4
        assert "less than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg_int = 4.5
        assert "less than" in str(excinfo.value)
        # Ensure 0 works if allow_zero is true
        if pos_neg_test.allow_zero:
            pos_neg_test.neg_int = 0
            assert pos_neg_test.neg_int == 0
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.neg_int = 4
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                pos_neg_test.neg_int = 0
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            pos_neg_test.neg_int = "hello world"


@pytest.fixture
def gt_lt_test(limit: float, inclusive: bool):
    class MyClass:

        gt = pt.greater_than(limit, inclusive=inclusive)
        gt_float = pt.float_greater_than(limit, inclusive=inclusive)
        gt_int = pt.int_greater_than(limit, inclusive=inclusive)
        lt = pt.less_than(limit, inclusive=inclusive)
        lt_float = pt.float_less_than(limit, inclusive=inclusive)
        lt_int = pt.int_less_than(limit, inclusive=inclusive)

        def __init__(self):
            self.limit = limit
            self.inclusive = inclusive

    return MyClass()


class TestGtLt:
    @pytest.mark.parametrize(
        "limit, inclusive",
        [(5, False), (5.5, True), (5.5, False), (5, True)],
    )
    def test_greater_than(self, gt_lt_test):
        limit = gt_lt_test.limit
        # Ensure the user can assign any number over limit
        gt_lt_test.gt = int(limit + 3)
        assert gt_lt_test.gt == int(limit + 3)
        assert isinstance(gt_lt_test.gt, int)
        gt_lt_test.gt = limit + 3.5
        assert gt_lt_test.gt == limit + 3.5
        assert isinstance(gt_lt_test.gt, float)
        # Ensure anything less than fails
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt = int(limit - 4)
        assert "greater than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt = limit - 6.2
        assert "greater than" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if gt_lt_test.inclusive:
            gt_lt_test.gt = limit
            assert gt_lt_test.gt == limit
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.gt = limit - 1
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.gt = limit
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt = "hello world"

    @pytest.mark.parametrize(
        "limit, inclusive",
        [(5, False), (5.5, True), (5.5, False), (5, True)],
    )
    def test_float_greater_than(self, gt_lt_test):
        limit = gt_lt_test.limit
        # Ensure the user can assign any float over limit
        gt_lt_test.gt_float = limit + 2.2
        assert gt_lt_test.gt_float == limit + 2.2
        assert isinstance(gt_lt_test.gt_float, float)
        # test that ints are converted
        gt_lt_test.gt_float = int(limit + 1)
        assert gt_lt_test.gt_float == int(limit + 1)
        assert isinstance(gt_lt_test.gt_float, float)
        # Ensure anything less than fails
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt_float = limit - 1.1
        assert "greater than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt_float = limit - 10
        assert "greater than" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if gt_lt_test.inclusive:
            gt_lt_test.gt_float = limit
            assert gt_lt_test.gt_float == limit
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.gt_float = limit - 1
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.gt_float = limit
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt_float = "hello world"

    @pytest.mark.parametrize(
        "limit, inclusive",
        [(5, False), (5.5, True), (5.5, False), (5, True)],
    )
    def test_int_greater_than(self, gt_lt_test):
        limit = gt_lt_test.limit
        # Ensure the user can assign any int over limit
        gt_lt_test.gt_int = limit + 7
        assert gt_lt_test.gt_int == int(limit + 7)
        assert isinstance(gt_lt_test.gt_int, int)
        # test that floats are converted
        gt_lt_test.gt_int = limit + 2.3
        assert gt_lt_test.gt_int == int(limit + 2.3)
        assert isinstance(gt_lt_test.gt_int, int)
        # Ensure anything less than fails
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt_int = limit - 1
        assert "greater than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt_int = limit - 0.1
        assert "greater than" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if gt_lt_test.inclusive:
            gt_lt_test.gt_int = limit
            assert gt_lt_test.gt_int == int(limit)
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.gt_int = limit - 1
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.gt_int = limit
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.gt_int = "hello world"

    @pytest.mark.parametrize(
        "limit, inclusive",
        [(5, False), (5.5, True), (5.5, False), (5, True)],
    )
    def test_less_than(self, gt_lt_test):
        limit = gt_lt_test.limit
        # Ensure the user can assign any number under limit
        gt_lt_test.lt = int(limit - 3)
        assert gt_lt_test.lt == int(limit - 3)
        assert isinstance(gt_lt_test.lt, int)
        gt_lt_test.lt = limit - 3.5
        assert gt_lt_test.lt == limit - 3.5
        assert isinstance(gt_lt_test.lt, float)
        # Ensure anything greater than fails
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt = int(limit + 4)
        assert "less than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt = limit + 6.2
        assert "less than" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if gt_lt_test.inclusive:
            gt_lt_test.lt = limit
            assert gt_lt_test.lt == limit
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.lt = limit + 1
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.lt = limit
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt = "hello world"

    @pytest.mark.parametrize(
        "limit, inclusive",
        [(5, False), (5.5, True), (5.5, False), (5, True)],
    )
    def test_float_less_than(self, gt_lt_test):
        limit = gt_lt_test.limit
        # Ensure the user can assign any float under limit
        gt_lt_test.lt_float = limit - 2.2
        assert gt_lt_test.lt_float == limit - 2.2
        assert isinstance(gt_lt_test.lt_float, float)
        # test that ints are converted
        gt_lt_test.lt_float = int(limit - 1)
        assert gt_lt_test.lt_float == int(limit - 1)
        assert isinstance(gt_lt_test.lt_float, float)
        # Ensure anything greater than fails
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt_float = limit + 1.1
        assert "less than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt_float = limit + 10
        assert "less than" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if gt_lt_test.inclusive:
            gt_lt_test.lt_float = limit
            assert gt_lt_test.lt_float == limit
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.lt_float = limit + 1
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.lt_float = limit
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt_float = "hello world"

    @pytest.mark.parametrize(
        "limit, inclusive",
        [(5, False), (5.5, True), (5.5, False), (5, True)],
    )
    def test_int_less_than(self, gt_lt_test):
        limit = gt_lt_test.limit
        # Ensure the user can assign any int under limit
        gt_lt_test.lt_int = limit - 7
        assert gt_lt_test.lt_int == int(limit - 7)
        assert isinstance(gt_lt_test.lt_int, int)
        # test that floats are converted
        gt_lt_test.lt_int = limit - 2.3
        assert gt_lt_test.lt_int == int(limit - 2.3)
        assert isinstance(gt_lt_test.lt_int, int)
        # Ensure anything greater than fails
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt_int = limit + 1
        assert "less than" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt_int = limit + 0.1
        assert "less than" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if gt_lt_test.inclusive:
            gt_lt_test.lt_int = limit
            assert gt_lt_test.lt_int == int(limit)
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.lt_int = limit + 1
            assert "or equal to" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                gt_lt_test.lt_int = limit
            assert "or equal to" not in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            gt_lt_test.lt_int = "hello world"


@pytest.fixture
def ranged_test(bounds: (float, float), inclusive: (bool, bool)):
    class MyClass:

        in_range = pt.in_range(bounds=bounds, inclusive=inclusive)
        float_in_range = pt.float_in_range(bounds=bounds, inclusive=inclusive)
        int_in_range = pt.int_in_range(bounds=bounds, inclusive=inclusive)
        not_in_range = pt.not_in_range(bounds=bounds, inclusive=inclusive)
        float_not_in_range = pt.float_not_in_range(bounds=bounds, inclusive=inclusive)
        int_not_in_range = pt.int_not_in_range(bounds=bounds, inclusive=inclusive)

        def __init__(self):
            self.bounds = bounds
            self.inclusive = inclusive
            if isinstance(inclusive, bool):
                self.inclusive = (inclusive, inclusive)

    return MyClass()


def get_ranged_params():
    return product(
        product((-2.2, -2), (+2.2, +2)),
        [*product((False, True), (False, True)), False, True],
    )


class TestRanged:
    @pytest.mark.parametrize("bounds, inclusive", get_ranged_params())
    def test_in_range(self, ranged_test):
        bounds = ranged_test.bounds
        inclusive = ranged_test.inclusive
        # Ensure the user can assign number within bounds
        ranged_test.in_range = 0.5 * sum(bounds)
        assert ranged_test.in_range == 0.5 * sum(bounds)
        assert isinstance(ranged_test.in_range, float)
        ranged_test.in_range = int(0.5 * sum(bounds))
        assert ranged_test.in_range == int(0.5 * sum(bounds))
        assert isinstance(ranged_test.in_range, int)
        # Ensure anything outside fails
        with pytest.raises(ValueError) as excinfo:
            ranged_test.in_range = bounds[0] - 1
        assert "range" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            ranged_test.in_range = bounds[1] + 1
        assert "range" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if ranged_test.inclusive[0]:
            ranged_test.in_range = bounds[0]
            assert ranged_test.in_range == bounds[0]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.in_range = bounds[0] - 1
            assert "[" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.in_range = bounds[0]
            assert "(" in str(excinfo.value)
        if ranged_test.inclusive[1]:
            ranged_test.in_range = bounds[1]
            assert ranged_test.in_range == bounds[1]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.in_range = bounds[1] + 1
            assert "]" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.in_range = bounds[1]
            assert ")" in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            ranged_test.in_range = "hello world"

    @pytest.mark.parametrize("bounds, inclusive", get_ranged_params())
    def test_float_in_range(self, ranged_test):
        bounds = ranged_test.bounds
        inclusive = ranged_test.inclusive
        # Ensure the user can assign number within bounds
        ranged_test.float_in_range = 0.5 * sum(bounds)
        assert ranged_test.float_in_range == 0.5 * sum(bounds)
        assert isinstance(ranged_test.float_in_range, float)
        ranged_test.float_in_range = int(0.5 * sum(bounds))
        assert ranged_test.float_in_range == int(0.5 * sum(bounds))
        assert isinstance(ranged_test.float_in_range, float)
        # Ensure anything outside fails
        with pytest.raises(ValueError) as excinfo:
            ranged_test.float_in_range = bounds[0] - 1
        assert "range" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            ranged_test.float_in_range = bounds[1] + 1
        # Ensure limit works if inclusive is true
        if ranged_test.inclusive[0]:
            ranged_test.float_in_range = bounds[0]
            assert ranged_test.float_in_range == bounds[0]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_in_range = bounds[0] - 1
            assert "[" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_in_range = bounds[0]
            assert "(" in str(excinfo.value)
        if ranged_test.inclusive[1]:
            ranged_test.float_in_range = bounds[1]
            assert ranged_test.float_in_range == bounds[1]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_in_range = bounds[1] + 1
            assert "]" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_in_range = bounds[1]
            assert ")" in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            ranged_test.float_in_range = "hello world"

    @pytest.mark.parametrize("bounds, inclusive", get_ranged_params())
    def test_int_in_range(self, ranged_test):
        bounds = ranged_test.bounds
        inclusive = ranged_test.inclusive
        # Ensure the user can assign number within bounds
        ranged_test.int_in_range = 0.5 * sum(bounds)
        assert ranged_test.int_in_range == int(0.5 * sum(bounds))
        assert isinstance(ranged_test.int_in_range, int)
        # Ensure anything outside fails
        with pytest.raises(ValueError) as excinfo:
            ranged_test.int_in_range = bounds[0] - 1
        assert "range" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            ranged_test.int_in_range = bounds[1] + 1
        # Ensure limit works if inclusive is true
        if ranged_test.inclusive[0]:
            ranged_test.int_in_range = bounds[0]
            assert ranged_test.int_in_range == int(bounds[0])
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_in_range = bounds[0] - 1
            assert "[" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_in_range = bounds[0]
            assert "(" in str(excinfo.value)
        if ranged_test.inclusive[1]:
            ranged_test.int_in_range = bounds[1]
            assert ranged_test.int_in_range == int(bounds[1])
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_in_range = bounds[1] + 1
            assert "]" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_in_range = bounds[1]
            assert ")" in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            ranged_test.int_in_range = "hello world"

    @pytest.mark.parametrize("bounds, inclusive", get_ranged_params())
    def test_not_in_range(self, ranged_test):
        bounds = ranged_test.bounds
        inclusive = ranged_test.inclusive
        # Ensure the user can assign number outside bounds
        ranged_test.not_in_range = bounds[0] - 1.1
        assert ranged_test.not_in_range == bounds[0] - 1.1
        assert isinstance(ranged_test.not_in_range, float)
        ranged_test.not_in_range = bounds[1] + 1.1
        assert ranged_test.not_in_range == bounds[1] + 1.1
        assert isinstance(ranged_test.not_in_range, float)
        ranged_test.not_in_range = int(bounds[0]) - 1
        assert ranged_test.not_in_range == int(bounds[0]) - 1
        assert isinstance(ranged_test.not_in_range, int)
        ranged_test.not_in_range = int(bounds[1]) + 1
        assert ranged_test.not_in_range == int(bounds[1]) + 1
        assert isinstance(ranged_test.not_in_range, int)
        # Ensure anything inside fails
        with pytest.raises(ValueError) as excinfo:
            ranged_test.not_in_range = 0.5 * sum(bounds)
        assert "range" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if ranged_test.inclusive[0]:
            ranged_test.not_in_range = bounds[0]
            assert ranged_test.not_in_range == bounds[0]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.not_in_range = bounds[0] + 1
            assert "[" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.not_in_range = bounds[0]
            assert "(" in str(excinfo.value)
        if ranged_test.inclusive[1]:
            ranged_test.not_in_range = bounds[1]
            assert ranged_test.not_in_range == bounds[1]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.not_in_range = bounds[1] - 1
            assert "]" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.not_in_range = bounds[1]
            assert ")" in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            ranged_test.not_in_range = "hello world"

    @pytest.mark.parametrize("bounds, inclusive", get_ranged_params())
    def test_float_not_in_range(self, ranged_test):
        bounds = ranged_test.bounds
        inclusive = ranged_test.inclusive
        # Ensure the user can assign number outside bounds
        ranged_test.float_not_in_range = bounds[0] - 1.1
        assert ranged_test.float_not_in_range == bounds[0] - 1.1
        assert isinstance(ranged_test.float_not_in_range, float)
        ranged_test.float_not_in_range = bounds[1] + 1.1
        assert ranged_test.float_not_in_range == bounds[1] + 1.1
        assert isinstance(ranged_test.float_not_in_range, float)
        ranged_test.float_not_in_range = int(bounds[0]) - 1
        assert ranged_test.float_not_in_range == int(bounds[0]) - 1
        assert isinstance(ranged_test.float_not_in_range, float)
        ranged_test.float_not_in_range = int(bounds[1]) + 1
        assert ranged_test.float_not_in_range == int(bounds[1]) + 1
        assert isinstance(ranged_test.float_not_in_range, float)
        # Ensure anything inside fails
        with pytest.raises(ValueError) as excinfo:
            ranged_test.float_not_in_range = 0.5 * sum(bounds)
        assert "range" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if ranged_test.inclusive[0]:
            ranged_test.float_not_in_range = bounds[0]
            assert ranged_test.float_not_in_range == bounds[0]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_not_in_range = bounds[0] + 1
            assert "[" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_not_in_range = bounds[0]
            assert "(" in str(excinfo.value)
        if ranged_test.inclusive[1]:
            ranged_test.float_not_in_range = bounds[1]
            assert ranged_test.float_not_in_range == bounds[1]
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_not_in_range = bounds[1] - 1
            assert "]" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.float_not_in_range = bounds[1]
            assert ")" in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            ranged_test.float_not_in_range = "hello world"

    @pytest.mark.parametrize("bounds, inclusive", get_ranged_params())
    def test_int_not_in_range(self, ranged_test):
        bounds = ranged_test.bounds
        inclusive = ranged_test.inclusive
        # Ensure the user can assign number outside bounds
        ranged_test.int_not_in_range = bounds[0] - 1.1
        assert ranged_test.int_not_in_range == int(bounds[0] - 1.1)
        assert isinstance(ranged_test.int_not_in_range, int)
        ranged_test.int_not_in_range = bounds[1] + 1.1
        assert ranged_test.int_not_in_range == int(bounds[1] + 1.1)
        assert isinstance(ranged_test.int_not_in_range, int)
        # Ensure anything inside fails
        with pytest.raises(ValueError) as excinfo:
            ranged_test.int_not_in_range = 0.5 * sum(bounds)
        assert "range" in str(excinfo.value)
        # Ensure limit works if inclusive is true
        if ranged_test.inclusive[0]:
            ranged_test.int_not_in_range = bounds[0]
            assert ranged_test.int_not_in_range == int(bounds[0])
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_not_in_range = bounds[0] + 1
            assert "[" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_not_in_range = bounds[0]
            assert "(" in str(excinfo.value)
        if ranged_test.inclusive[1]:
            ranged_test.int_not_in_range = bounds[1]
            assert ranged_test.int_not_in_range == int(bounds[1])
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_not_in_range = bounds[1] - 1
            assert "]" in str(excinfo.value)
        else:
            with pytest.raises(ValueError) as excinfo:
                ranged_test.int_not_in_range = bounds[1]
            assert ")" in str(excinfo.value)
        # Ensure it won't allow non-numbers
        with pytest.raises(ValueError) as excinfo:
            ranged_test.int_not_in_range = "hello world"
