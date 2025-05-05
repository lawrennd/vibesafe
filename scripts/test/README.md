# VibeSafe Script Tests

This directory contains tests for VibeSafe scripts using the Bats (Bash Automated Testing System) framework.

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

## Running the Tests

From the repository root, run:

```bash
bats scripts/test/*.bats
```

Or to run a specific test file:

```bash
bats scripts/test/install-test.bats
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