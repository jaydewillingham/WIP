# Contributing to GLUMF

Thank you for your interest in contributing to GLUMF! This document provides guidelines and instructions for contributing.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Detailed steps** to reproduce
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, GLUMF version)
- **Code sample** demonstrating the issue
- **Error messages** (full traceback)

Example bug report:
```markdown
**Bug:** fit_schechter_emcee fails with negative luminosities

**Steps to reproduce:**
1. Load data with `load_excel_sheets()`
2. Call `fit_schechter_emcee()` with log luminosities < 0
3. See error

**Expected:** Function should handle or warn about invalid input
**Actual:** Crashes with ValueError

**Environment:**
- OS: Ubuntu 20.04
- Python: 3.9.7
- GLUMF: 1.0.0

**Traceback:**
```
ValueError: ...
```
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear title** and description
- **Use case** explaining why this would be useful
- **Proposed solution** (if you have one)
- **Alternatives considered**

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation**
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

## Development Setup

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/glumf.git
cd glumf

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Run tests
python tests/test_basic.py
python tests/test_plotting.py

# Or with pytest
pytest tests/
```

### 3. Development Workflow

```bash
# Make changes to code
vim glumf/core.py

# Run tests
pytest tests/

# Check code style
flake8 glumf/

# Run examples
cd examples
python complete_workflow.py
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Organized (standard library, third-party, local)
- **Docstrings**: NumPy style

### Example Code Style

```python
"""
Module docstring explaining purpose.
"""

import numpy as np
import pandas as pd
from scipy import stats

from glumf.core import schechter


def my_function(param1, param2, param3=None):
    """
    One-line summary of function.
    
    More detailed description if needed. Explain what the function
    does, not how it does it.
    
    Parameters
    ----------
    param1 : array-like
        Description of param1
    param2 : float
        Description of param2
    param3 : str, optional
        Description of param3 (default: None)
        
    Returns
    -------
    dict
        Description of return value
        
    Examples
    --------
    >>> result = my_function([1, 2, 3], 0.5)
    >>> print(result['key'])
    value
    """
    # Implementation with clear variable names
    intermediate_result = param1 * param2
    
    if param3 is not None:
        # Handle optional parameter
        final_result = process(intermediate_result, param3)
    else:
        final_result = intermediate_result
    
    return {'key': final_result}
```

### Documentation Style

Use NumPy-style docstrings:

```python
def schechter(L, phi_star, L_star, alpha):
    """
    Compute the Schechter luminosity function.
    
    The Schechter function describes the number density of galaxies
    as a function of luminosity.
    
    Parameters
    ----------
    L : array-like
        Luminosity values in erg/s
    phi_star : float
        Normalization parameter in Mpc^-3 dex^-1
    L_star : float
        Characteristic luminosity in erg/s
    alpha : float
        Faint-end slope parameter
        
    Returns
    -------
    array-like
        Schechter function values in Mpc^-3 dex^-1
        
    Notes
    -----
    The Schechter function is defined as:
    
    .. math::
        \\phi(L) = \\phi^* (L/L^*)^\\alpha \\exp(-L/L^*) (L/L^*) \\ln(10)
    
    Examples
    --------
    >>> L = np.logspace(40, 43, 100)
    >>> phi = schechter(L, 1e-3, 1e42, -1.5)
    >>> plt.plot(np.log10(L), np.log10(phi))
    """
    # Implementation
    pass
```

## Testing Guidelines

### Writing Tests

All new features must include tests. Place tests in `tests/` directory.

```python
"""
Test module for new feature.
"""

import numpy as np
import pytest
from glumf import my_new_function


def test_basic_functionality():
    """Test basic usage of my_new_function."""
    result = my_new_function(input_data)
    assert result == expected_output


def test_edge_cases():
    """Test edge cases."""
    # Test with empty input
    result = my_new_function([])
    assert result is None
    
    # Test with invalid input
    with pytest.raises(ValueError):
        my_new_function(-1)


def test_numerical_accuracy():
    """Test numerical accuracy."""
    result = my_new_function(test_data)
    np.testing.assert_allclose(result, expected, rtol=1e-5)
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=glumf tests/

# Run with verbose output
pytest -v tests/
```

### Test Coverage

Aim for >80% code coverage for new features:

```bash
pytest --cov=glumf --cov-report=html tests/
# Open htmlcov/index.html to view coverage
```

## Documentation

### Updating README

When adding features:
1. Add to feature list
2. Add usage example
3. Update API reference
4. Add to table of contents if needed

### Updating API Documentation

For new functions/classes:
1. Add comprehensive docstring
2. Add to `__all__` in `__init__.py`
3. Add example in README
4. Add to API Reference section

### Writing Examples

Good examples are:
- **Self-contained**: Can be run independently
- **Commented**: Explain what each step does
- **Realistic**: Use realistic data/parameters
- **Complete**: Include imports and setup

## Pull Request Process

### Before Submitting

- [ ] Tests pass (`pytest tests/`)
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Docstrings added/updated
- [ ] Examples added (if applicable)
- [ ] CHANGELOG.md updated

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
Describe tests added/modified

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code style follows guidelines
- [ ] Self-review completed

## Related Issues
Fixes #123
```

### Review Process

1. Automated tests run on PR
2. Code review by maintainer(s)
3. Address feedback
4. Approval and merge

### After Merge

- PR branch will be deleted
- Changes included in next release
- Credit added to CHANGELOG

## Questions?

- Open an issue for discussion
- Email: your.email@example.com

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in CHANGELOG.md
- Thanked in release notes

Thank you for contributing to GLUMF! 🌟
