# VibeSafe Test Suite

This directory contains tests for VibeSafe scripts and functionality.

## Running Tests

To run all tests:

```bash
bats scripts/test/*.bats
```

To run a specific test file:

```bash
bats scripts/test/install-test.bats
```

## Test Coverage

### Prerequisites

To generate test coverage reports, you need [kcov](https://github.com/SimonKagstrom/kcov) installed:

- On Ubuntu/Debian: `sudo apt-get install kcov`
- On macOS: `brew install kcov`

### Running Tests with Coverage

Use the provided script to run tests with coverage:

```bash
./scripts/run-tests-with-coverage.sh
```

This will:
1. Run all tests with kcov to track coverage
2. Generate an HTML coverage report in the `coverage/` directory
3. Display a summary of the coverage results

### Viewing Coverage Reports

Open `coverage/index.html` in your browser to view the detailed coverage report.

### CI Integration

When running in GitHub Actions, test coverage is automatically uploaded to [Codecov](https://codecov.io).

## Writing Tests

Tests are written using [Bats](https://github.com/bats-core/bats-core) (Bash Automated Testing System).

### Basic Test Structure

```bash
#!/usr/bin/env bats

setup() {
  # Code to run before each test
}

teardown() {
  # Code to run after each test
}

@test "Test name" {
  # Test code
  [ true ]  # Assertion
}
```

### Test Examples

See the existing `.bats` files in this directory for examples of how to write tests.

## Prerequisites

To run these tests locally, you'll need to install Bats:

### On macOS:
```bash
brew install bats-core
```

### On Ubuntu/Debian:
```bash
sudo apt-get install bats
```

### On other systems or to install from source:
```bash
git clone https://github.com/bats-core/bats-core.git
cd bats-core
./install.sh /usr/local
```

## Test Structure

Each test file follows this general structure:

1. `setup()` - Prepares the environment for testing
2. `teardown()` - Cleans up after the test
3. Individual test cases using the `@test` decorator

## Adding New Tests

To add new tests:

1. Create a new `.bats` file in this directory
2. Follow the pattern in existing test files
3. Use the `@test` decorator to define test cases
4. Implement assertions using standard Bash test commands and Bats utilities

## Continuous Integration

These tests are integrated with our GitHub Actions workflow to ensure scripts work reliably across all supported platforms.

## More Information

- [Bats GitHub Repository](https://github.com/bats-core/bats-core)
- [Bats Documentation](https://bats-core.readthedocs.io/) 