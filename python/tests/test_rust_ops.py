"""Unit tests for the Rust-backed functions exposed via mixedlib.rust."""

import pytest

from mixedlib.rust import divide_rust, multiply_rust


class TestMultiplyRust:
    def test_positive_integers(self):
        assert multiply_rust(3, 4) == 12

    def test_negative_factor(self):
        assert multiply_rust(-2, 5) == -10

    def test_by_zero(self):
        assert multiply_rust(0, 100) == 0

    def test_floats(self):
        assert multiply_rust(1.5, 2.0) == pytest.approx(3.0)

    def test_both_negative(self):
        assert multiply_rust(-3, -4) == 12


class TestDivideRust:
    def test_exact_division(self):
        assert divide_rust(10, 2) == pytest.approx(5.0)

    def test_decimal_result(self):
        assert divide_rust(7, 2) == pytest.approx(3.5)

    def test_negative_dividend(self):
        assert divide_rust(-9, 3) == pytest.approx(-3.0)

    def test_negative_divisor(self):
        assert divide_rust(9, -3) == pytest.approx(-3.0)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            divide_rust(1, 0)

    def test_divide_zero_by_nonzero(self):
        assert divide_rust(0, 5) == pytest.approx(0.0)
