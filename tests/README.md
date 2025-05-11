# VibeSafe Tests

This directory contains tests for the VibeSafe project, focusing on Python component tests.

## Test Organization

The tests are organized as follows:

- `test_whats_next.py`: Tests for the "What's Next" script (`scripts/whats_next.py`)

## Running Tests

### Using pytest directly:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=scripts/ --cov-report=html
```

### Using the provided script:

```bash
# Run all Python tests with coverage
./scripts/run-python-tests.sh
```

### Integration with the main test suite:

The Python tests are automatically integrated with the existing test suite:

```bash
# Run all tests (including Bats tests and Python tests)
./scripts/run-tests-with-coverage.sh
```

## GitHub Actions Integration

These tests are integrated into the GitHub Actions CI pipeline:

1. The `python-tests.yml` workflow runs Python tests on multiple Python versions
2. The `test-coverage.yml` workflow includes Python test coverage in the overall coverage report

## Writing New Tests

When writing new tests:

1. Create test files named `test_*.py` in this directory
2. Use Python's built-in `unittest` framework or `pytest`
3. Ensure tests are isolated and don't depend on external state
4. Mock external dependencies (e.g., file system, Git commands) using `unittest.mock`

## Coverage Requirements

We aim for high test coverage in the Python components:

- Minimum test coverage goal: 80%
- Each new feature should include appropriate test cases
- Tests should cover both success and error paths 