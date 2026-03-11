"""mixedlib — basic arithmetic with Python and Rust implementations.

Usage::

    from mixedlib import add, subtract, multiply, divide

``multiply`` and ``divide`` delegate to Rust functions in
``mixedlib.rust`` (backed by ``rust/src/lib.rs``).
"""

from mixedlib.rust import divide_rust, multiply_rust

__all__ = ["add", "subtract", "multiply", "divide"]


def add(a: float, b: float) -> float:
    """Return *a* + *b*."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return *a* - *b*."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return *a* × *b* (delegates to Rust ``multiply_rust``)."""
    return multiply_rust(a, b)


def divide(a: float, b: float) -> float:
    """Return *a* / *b* (delegates to Rust ``divide_rust``).

    Raises :exc:`ZeroDivisionError` if *b* is zero.
    """
    return divide_rust(a, b)
