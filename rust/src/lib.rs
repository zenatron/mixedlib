// ---------------------------------------------------------------------------
// Pure-Rust implementations — no PyO3 dependency.
// These are compiled (and unit-tested) with plain `cargo test`.
// ---------------------------------------------------------------------------

fn multiply_impl(a: f64, b: f64) -> f64 {
    a * b
}

fn divide_impl(a: f64, b: f64) -> Result<f64, &'static str> {
    if b == 0.0 {
        Err("division by zero")
    } else {
        Ok(a / b)
    }
}

// ---------------------------------------------------------------------------
// PyO3 bindings — only compiled when the `extension-module` feature is active.
// maturin always passes `--features extension-module`; plain `cargo test`
// does not, so no Python runtime or headers are needed to run the Rust tests.
// ---------------------------------------------------------------------------

#[cfg(feature = "extension-module")]
mod python_bindings {
    use pyo3::prelude::*;

    use super::{divide_impl, multiply_impl};

    /// Multiply two numbers.
    ///
    /// Exposed to Python as ``mixedlib.rust.multiply_rust``
    /// (via ``python/mixedlib/rust/__init__.py``) and as the lower-level
    /// ``mixedlib._rust.multiply_rust``.
    #[pyfunction]
    pub fn multiply_rust(a: f64, b: f64) -> f64 {
        multiply_impl(a, b)
    }

    /// Divide *a* by *b*.
    ///
    /// Exposed to Python as ``mixedlib.rust.divide_rust``
    /// (via ``python/mixedlib/rust/__init__.py``) and as the lower-level
    /// ``mixedlib._rust.divide_rust``.
    ///
    /// # Errors
    /// Raises ``ZeroDivisionError`` if *b* is zero.
    #[pyfunction]
    pub fn divide_rust(a: f64, b: f64) -> PyResult<f64> {
        divide_impl(a, b).map_err(|e| PyErr::new::<pyo3::exceptions::PyZeroDivisionError, _>(e))
    }

    // The module name must match the [lib] name in Cargo.toml ("_rust") and
    // the leaf of module-name in pyproject.toml ("mixedlib._rust").
    #[pymodule]
    pub fn _rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(multiply_rust, m)?)?;
        m.add_function(wrap_pyfunction!(divide_rust, m)?)?;
        Ok(())
    }
}

// Re-export so the #[pymodule] init symbol is at the crate root.
#[cfg(feature = "extension-module")]
pub use python_bindings::*;

// ---------------------------------------------------------------------------
// Unit tests (run with `cargo test` — no Python needed)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    // --- multiply ---

    #[test]
    fn test_multiply_positive_integers() {
        assert_eq!(multiply_impl(3.0, 4.0), 12.0);
    }

    #[test]
    fn test_multiply_negative() {
        assert_eq!(multiply_impl(-2.0, 5.0), -10.0);
    }

    #[test]
    fn test_multiply_by_zero() {
        assert_eq!(multiply_impl(0.0, 100.0), 0.0);
    }

    #[test]
    fn test_multiply_floats() {
        assert!((multiply_impl(1.5, 2.0) - 3.0).abs() < f64::EPSILON);
    }

    // --- divide ---

    #[test]
    fn test_divide_exact() {
        assert_eq!(divide_impl(10.0, 2.0), Ok(5.0));
    }

    #[test]
    fn test_divide_decimal_result() {
        assert_eq!(divide_impl(7.0, 2.0), Ok(3.5));
    }

    #[test]
    fn test_divide_negative_dividend() {
        assert_eq!(divide_impl(-9.0, 3.0), Ok(-3.0));
    }

    #[test]
    fn test_divide_by_zero_returns_err() {
        assert!(divide_impl(1.0, 0.0).is_err());
    }
}
