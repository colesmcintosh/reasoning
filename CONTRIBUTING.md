# Contributing to Reasoning Framework

Thank you for your interest in contributing to the Reasoning Framework! We welcome contributions from the community and are excited to have you help make this project better.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/colesmcintosh/reasoning.git
   cd reasoning
   ```
3. Install Poetry (if you haven't already):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
4. Install dependencies and set up the development environment:
   ```bash
   poetry install --all-extras
   poetry shell
   ```

## Development Process

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```

2. Make your changes, ensuring you:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. Run the test suite:
   ```bash
   poetry run pytest
   ```

4. Push to your fork:
   ```bash
   git push origin feature-name
   ```

5. Open a Pull Request on GitHub

## Code Style

- We follow PEP 8 guidelines
- Type hints are required for all new code
- Docstrings should follow the Google style

## Testing

- All new features should include tests
- Tests are written using pytest
- Aim for 100% test coverage on new code
- Run the full test suite before submitting a PR

## Documentation

- Update the README.md if you change functionality
- Add docstrings to all new functions and classes
- Update the documentation in the `docs/` directory
- Examples should be included for new features

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation with details of any new features
3. The PR should pass all CI checks
4. Get at least one code review from a maintainer
5. Once approved, a maintainer will merge your PR

## Reporting Issues

- Use the GitHub issue tracker
- Include Python version and operating system
- Provide a minimal reproducible example
- Include any relevant error messages
- Describe expected vs actual behavior

## Feature Requests

- Use the GitHub issue tracker
- Clearly describe the feature and its use case
- Discuss potential implementation approaches
- Be patient and open to feedback

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Questions?

If you have questions about contributing, feel free to:
- Open an issue
- Start a GitHub Discussion
- Reach out to the maintainers

## License

By contributing to Reasoning Framework, you agree that your contributions will be licensed under the MIT License. 