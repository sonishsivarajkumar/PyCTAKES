# Contributing to pyCTAKES

We welcome contributions to pyCTAKES! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please be respectful and constructive in all interactions.

## Getting Started

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/pyCTAKES.git
   cd pyCTAKES
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=pyctakes --cov-report=html
```

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
black src tests
isort src tests
flake8 src tests
mypy src/pyctakes
```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Python version and environment details
- Code snippets or error messages

### Suggesting Features

Feature requests are welcome! Please include:

- A clear description of the feature
- The motivation/use case
- Any relevant examples or mockups
- Consideration of alternatives

### Pull Requests

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following our coding standards
3. Add or update tests as needed
4. Update documentation if necessary
5. Ensure all tests pass and code is properly formatted
6. Commit your changes with clear, descriptive messages
7. Push to your fork and create a pull request

#### Pull Request Guidelines

- Target the `develop` branch (not `main`)
- Include a clear description of changes
- Reference any related issues
- Ensure CI checks pass
- Keep changes focused and atomic
- Update documentation for user-facing changes

### Writing Annotators

pyCTAKES is designed to be extensible through custom annotators. When contributing new annotators:

1. Inherit from `pyctakes.annotators.base.Annotator`
2. Implement required methods (`initialize`, `annotate`)
3. Add comprehensive tests
4. Include example usage in docstrings
5. Consider performance implications
6. Document configuration options

Example:
```python
from pyctakes.annotators.base import Annotator
from pyctakes.types import Document, Annotation

class MyAnnotator(Annotator):
    def initialize(self):
        # Load models, resources, etc.
        pass
    
    def annotate(self, document: Document):
        # Process document and return annotations
        return []
```

### Documentation

Documentation is built with Sphinx and hosted on ReadTheDocs. To build locally:

```bash
cd docs
make html
```

When contributing:
- Update docstrings for new/changed code
- Add examples for new features
- Update user guides as needed
- Use clear, concise language

### Testing Guidelines

- Write tests for all new functionality
- Aim for high test coverage (95%+)
- Use descriptive test names
- Include edge cases and error conditions
- Use fixtures for common test data
- Mock external dependencies

Test organization:
- Unit tests in `tests/`
- Integration tests in `tests/integration/`
- Performance tests in `tests/performance/`

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

The release process:
1. Updates to `develop` branch
2. Code review and testing
3. Merge to `main` branch
4. Create release tag
5. Automated build and PyPI publication

## Community

- **GitHub Discussions**: For questions and general discussion
- **Issues**: For bug reports and feature requests
- **Slack**: [Join our workspace](#) for real-time chat
- **Monthly Calls**: Community video calls (calendar link)

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to pyCTAKES!
