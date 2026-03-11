"""Unit tests for the pure-Python operations: add and subtract,
and the Python-level multiply / divide wrappers."""

import pytest

from mixedlib import add, divide, multiply, subtract


class TestAdd:
    def test_positive_integers(self):
        assert add(2, 3) == 5

    def test_negative(self):
        assert add(-1, -4) == -5

    def test_mixed_sign(self):
        assert add(-3, 7) == 4

    def test_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_zero(self):
        assert add(0, 0) == 0


class TestSubtract:
    def test_positive_result(self):
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        assert subtract(3, 10) == -7

    def test_floats(self):
        assert subtract(5.5, 2.5) == pytest.approx(3.0)

    def test_zero(self):
        assert subtract(0, 0) == 0


class TestMultiply:
    """multiply() is a Python wrapper that delegates to multiply_rust."""

    def test_positive_integers(self):
        assert multiply(3, 4) == 12

    def test_negative(self):
        assert multiply(-2, 5) == -10

    def test_by_zero(self):
        assert multiply(0, 999) == 0

    def test_floats(self):
        assert multiply(1.5, 2.0) == pytest.approx(3.0)


class TestDivide:
    """divide() is a Python wrapper that delegates to divide_rust."""

    def test_exact_division(self):
        assert divide(10, 2) == pytest.approx(5.0)

    def test_decimal_result(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_negative_dividend(self):
        assert divide(-9, 3) == pytest.approx(-3.0)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            divide(1, 0)
