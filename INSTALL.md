# Installation Guide for GLUMF

This guide provides detailed instructions for installing and setting up the GLUMF package.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Verification](#verification)
4. [Troubleshooting](#troubleshooting)
5. [Development Installation](#development-installation)

## Prerequisites

### Python Version
GLUMF requires Python 3.7 or higher. Check your Python version:

```bash
python --version
# or
python3 --version
```

If you need to install or upgrade Python, visit [python.org](https://www.python.org/downloads/).

### Recommended: Virtual Environment

We strongly recommend using a virtual environment to avoid dependency conflicts:

```bash
# Create a virtual environment
python -m venv glumf_env

# Activate it
# On Linux/Mac:
source glumf_env/bin/activate

# On Windows:
glumf_env\Scripts\activate
```

## Installation Methods

### Method 1: Install from Source (Recommended)

1. **Clone or download the repository:**

```bash
# If you have git:
git clone https://github.com/yourusername/glumf.git
cd glumf

# Or download and extract the ZIP file, then:
cd glumf
```

2. **Install the package:**

```bash
# Install in normal mode
pip install .

# Or install in editable/development mode (recommended for testing)
pip install -e .
```

3. **Install with development dependencies (optional):**

```bash
pip install -e ".[dev]"
```

This installs additional packages like `pytest` and `jupyter` for development and testing.

### Method 2: Install from requirements.txt

If you only want to install the dependencies without installing the package:

```bash
pip install -r requirements.txt
```

Then add the glumf directory to your Python path when using it.

## Verification

### Quick Test

After installation, verify that glumf is correctly installed:

```bash
python -c "import glumf; print(glumf.__version__)"
```

You should see: `1.0.0`

### Run Basic Tests

```bash
cd tests
python test_basic.py
```

Expected output:
```
==============================================================
GLUMF PACKAGE FUNCTIONALITY TESTS
==============================================================

==============================================================
TEST 1: Data Loading
==============================================================
Loading data from: ../data/Ha_Database_20250501.xlsx
✓ Loaded 28 sheets
...

==============================================================
ALL TESTS PASSED! ✓
==============================================================
```

### Run Plotting Tests

```bash
cd tests
python test_plotting.py
```

This will generate several test plots and verify the plotting functionality.

## Package Structure

After installation, your glumf directory should look like this:

```
glumf/
├── glumf/                  # Main package directory
│   ├── __init__.py
│   ├── core.py            # Core functions (Schechter fitting)
│   ├── data_loader.py     # Data loading utilities
│   ├── models.py          # SFR conversion and CSFD models
│   └── plotting.py        # Plotting functions
├── data/                  # Data files
│   ├── Ha_Database_20250501.xlsx
│   └── EMU_GAMA_20250902
├── tests/                 # Test scripts
│   ├── test_basic.py
│   └── test_plotting.py
├── examples/              # Example scripts
│   └── complete_workflow.py
├── setup.py
├── README.md
├── requirements.txt
└── LICENSE
```

## Troubleshooting

### Issue: ModuleNotFoundError for glumf

**Problem:** After installation, Python cannot find the glumf module.

**Solution:**
1. Make sure you're in the correct virtual environment
2. Verify installation: `pip list | grep glumf`
3. If using editable mode, ensure you're in the correct directory
4. Try reinstalling: `pip uninstall glumf && pip install -e .`

### Issue: Import errors for dependencies

**Problem:** Errors like `ModuleNotFoundError: No module named 'lmfit'`

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install specific missing package
pip install lmfit
```

### Issue: Excel file reading errors

**Problem:** `xlrd.biffh.XLRDError` or similar when reading Excel files

**Solution:**
```bash
pip install openpyxl
```

The package uses `openpyxl` to read `.xlsx` files.

### Issue: emcee installation problems

**Problem:** Errors during `emcee` installation

**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Then install emcee
pip install emcee

# If still failing, try installing from conda
conda install -c conda-forge emcee
```

### Issue: Matplotlib backend errors

**Problem:** Plotting fails with `_tkinter.TclError` or backend errors

**Solution:**
```bash
# Set matplotlib to use a different backend
export MPLBACKEND=Agg

# Or in Python code, add before importing glumf:
import matplotlib
matplotlib.use('Agg')
```

### Issue: Permission errors during installation

**Problem:** `PermissionError` when installing

**Solution:**
```bash
# Use --user flag
pip install --user -e .

# Or use sudo (not recommended)
sudo pip install .
```

## Development Installation

For developers who want to contribute to glumf:

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/glumf.git
cd glumf
```

2. **Install in editable mode with dev dependencies:**
```bash
pip install -e ".[dev]"
```

3. **Run tests:**
```bash
# Basic tests
python tests/test_basic.py

# Plotting tests
python tests/test_plotting.py

# Or use pytest (if installed)
pytest tests/
```

4. **Run the complete workflow example:**
```bash
cd examples
python complete_workflow.py
```

## Updating GLUMF

To update to the latest version:

```bash
cd glumf
git pull  # If using git
pip install --upgrade -e .
```

## Uninstalling

To remove glumf:

```bash
pip uninstall glumf
```

## System Requirements

### Minimum Requirements
- Python 3.7+
- 2 GB RAM
- 500 MB disk space

### Recommended Requirements
- Python 3.9+
- 4+ GB RAM (for MCMC fitting)
- 1 GB disk space

## Platform-Specific Notes

### Windows
- Use `python` instead of `python3`
- Use backslashes (`\`) in paths or use raw strings
- If matplotlib doesn't work, try installing from conda-forge

### macOS
- May need Xcode command line tools: `xcode-select --install`
- Use `python3` explicitly

### Linux
- Most distributions should work out of the box
- Install development headers if compilation is needed:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-dev
  
  # Fedora/RHEL
  sudo dnf install python3-devel
  ```

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) for general usage
2. Look at example scripts in `examples/`
3. Review test scripts in `tests/`
4. Open an issue on GitHub (if applicable)
5. Contact: your.email@example.com

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage examples
2. Run the complete workflow: `python examples/complete_workflow.py`
3. Try the quick start examples in the README
4. Explore the API documentation in the README

Enjoy using GLUMF! 🌟
