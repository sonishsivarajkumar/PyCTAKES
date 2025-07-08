# Contributing to PyCTAKES

Thank you for your interest in contributing to PyCTAKES! This guide will help you get started with contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub
   git clone https://github.com/YOUR_USERNAME/pyctakes.git
   cd pyctakes
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Verify Setup**
   ```bash
   python -m pytest tests/
   python -m pyctakes --help
   ```

## Development Workflow

### Creating a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add: description of your changes"

# Push branch
git push origin feature/your-feature-name
```

### Code Style and Quality

PyCTAKES uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

Run quality checks:
```bash
# Format code
black src/ tests/
isort src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest tests/
```

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pipeline.py

# Run with coverage
pytest --cov=pyctakes tests/

# Run integration tests
pytest tests/test_integrated_pipeline.py -v
```

#### Writing Tests

Create tests for new functionality:

```python
# tests/test_new_feature.py
import pytest
from pyctakes.types import Document
from pyctakes.your_module import YourClass

class TestYourClass:
    def setup_method(self):
        """Setup for each test method."""
        self.instance = YourClass()
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        doc = Document(text="Test input")
        result = self.instance.process(doc)
        
        assert result is not None
        assert len(result.annotations) > 0
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Empty input
        doc = Document(text="")
        result = self.instance.process(doc)
        assert len(result.annotations) == 0
        
        # Very long input
        long_text = "word " * 10000
        doc = Document(text=long_text)
        result = self.instance.process(doc)
        assert result is not None
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            YourClass(invalid_param="invalid")
```

## Contribution Types

### Bug Fixes

1. **Identify the Issue**
   - Search existing issues
   - Create new issue if needed
   - Discuss approach with maintainers

2. **Fix the Bug**
   - Write failing test that reproduces bug
   - Implement fix
   - Ensure test passes
   - Verify no regressions

3. **Submit Pull Request**
   - Reference issue number
   - Describe fix clearly
   - Include test coverage

### New Features

1. **Propose Feature**
   - Create feature request issue
   - Discuss design with maintainers
   - Get approval before implementing

2. **Implement Feature**
   - Follow existing code patterns
   - Add comprehensive tests
   - Update documentation
   - Add examples if needed

3. **Submit Pull Request**
   - Reference feature request
   - Explain implementation
   - Demonstrate usage

### Documentation

1. **Identify Documentation Needs**
   - Missing documentation
   - Unclear explanations
   - Outdated information

2. **Improve Documentation**
   - Update markdown files
   - Add code examples
   - Improve docstrings
   - Test documentation examples

## Code Guidelines

### Python Style

Follow PEP 8 and project conventions:

```python
# Good: Clear, descriptive names
class ClinicalNERAnnotator:
    def __init__(self, approach: str = "rule_based"):
        self.approach = approach
    
    def process(self, doc: Document) -> Document:
        """Process document to extract clinical entities."""
        return self._extract_entities(doc)

# Good: Type hints and docstrings
def create_default_pipeline(config: Optional[Dict[str, Any]] = None) -> Pipeline:
    """
    Create default clinical NLP pipeline.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured pipeline instance
    """
    pipeline = Pipeline()
    # ... implementation
    return pipeline
```

### Architecture Patterns

Follow established patterns:

```python
# Annotator pattern
class NewAnnotator(BaseAnnotator):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = kwargs
    
    def process(self, doc: Document) -> Document:
        # Implementation
        return doc

# Configuration pattern
def create_annotator_from_config(config: Dict[str, Any]) -> BaseAnnotator:
    annotator_type = config.get("type", "default")
    
    if annotator_type == "new":
        return NewAnnotator(**config.get("options", {}))
    else:
        raise ValueError(f"Unknown annotator type: {annotator_type}")
```

### Error Handling

Use consistent error handling:

```python
from pyctakes.exceptions import PyCTAKESError, AnnotationError

class CustomAnnotator(BaseAnnotator):
    def process(self, doc: Document) -> Document:
        try:
            return self._process_safely(doc)
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise AnnotationError(f"CustomAnnotator failed: {e}") from e
```

## Documentation Guidelines

### Docstring Format

Use Google-style docstrings:

```python
def process_clinical_text(text: str, pipeline: Pipeline) -> Document:
    """
    Process clinical text using specified pipeline.
    
    Args:
        text: Clinical text to process
        pipeline: PyCTAKES pipeline instance
        
    Returns:
        Processed document with annotations
        
    Raises:
        AnnotationError: If processing fails
        
    Example:
        >>> pipeline = create_default_pipeline()
        >>> doc = process_clinical_text("Patient has diabetes.", pipeline)
        >>> print(len(doc.entities))
        1
    """
```

### README Updates

Update README.md for significant changes:

- New features in feature list
- Installation instructions
- Usage examples
- API changes

### API Documentation

Update API docs for new classes/methods:

```markdown
## NewAnnotator

::: pyctakes.annotators.new.NewAnnotator
    options:
      show_source: false
      heading_level: 3
```

## Pull Request Process

### Before Submitting

1. **Ensure Quality**
   ```bash
   # Run full test suite
   pytest tests/
   
   # Check code quality
   pre-commit run --all-files
   
   # Verify documentation builds
   mkdocs build
   ```

2. **Update Documentation**
   - Add docstrings to new functions/classes
   - Update user guides if needed
   - Add examples for new features

3. **Update Changelog**
   ```markdown
   ## [Unreleased]
   
   ### Added
   - New feature description
   
   ### Fixed
   - Bug fix description
   ```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Added tests for new functionality
- [ ] All tests pass
- [ ] Manual testing completed

## Documentation
- [ ] Updated docstrings
- [ ] Updated user documentation
- [ ] Added examples

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs
   - Code quality checks
   - Test coverage

2. **Manual Review**
   - Code review by maintainers
   - Documentation review
   - Testing verification

3. **Feedback Integration**
   - Address review comments
   - Update code as needed
   - Re-request review

## Release Process

### Version Numbering

PyCTAKES follows semantic versioning:
- **Major**: Breaking changes (1.0.0 → 2.0.0)
- **Minor**: New features (1.0.0 → 1.1.0)
- **Patch**: Bug fixes (1.0.0 → 1.0.1)

### Release Checklist

1. **Prepare Release**
   - Update version in `pyproject.toml`
   - Update CHANGELOG.md
   - Update documentation

2. **Create Release**
   - Tag release: `git tag v1.0.0`
   - Push tags: `git push --tags`
   - GitHub Actions handles PyPI release

3. **Post-Release**
   - Verify PyPI package
   - Update documentation site
   - Announce release

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

### Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas
- **Pull Requests**: Code changes

### Getting Help

- Check existing documentation
- Search closed issues
- Ask questions in discussions
- Tag maintainers if urgent

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Documentation credits

Thank you for contributing to PyCTAKES! 🎉
