# GLUMF Project Structure

This document describes the organization of the GLUMF package.

## Directory Tree

```
glumf/
├── glumf/                          # Main package directory
│   ├── __init__.py                # Package initialization, exports
│   ├── core.py                    # Core Schechter fitting functions
│   ├── data_loader.py             # Data loading and preprocessing
│   ├── models.py                  # SFR conversion and CSFD models
│   └── plotting.py                # Visualization functions
│
├── data/                          # Data files
│   ├── Ha_Database_20250501.xlsx  # H-alpha luminosity function database
│   └── EMU_GAMA_20250902          # EMU-GAMA FITS data
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_basic.py              # Core functionality tests
│   └── test_plotting.py           # Plotting tests
│
├── examples/                      # Example scripts
│   ├── __init__.py
│   └── complete_workflow.py       # Full analysis pipeline example
│
├── setup.py                       # Package installation configuration
├── requirements.txt               # Python dependencies
├── MANIFEST.in                    # Additional files for distribution
├── .gitignore                     # Git ignore patterns
│
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── INSTALL.md                     # Installation instructions
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history
├── LICENSE                        # MIT License
├── PROJECT_STRUCTURE.md           # This file
│
└── verify_installation.py         # Installation verification script
```

## File Descriptions

### Package Core (`glumf/`)

#### `__init__.py`
- Package initialization
- Exports main functions for easy import
- Version information
- Defines `__all__` for `from glumf import *`

#### `core.py` (350 lines)
Core functionality for Schechter function analysis:
- `schechter()`: Schechter luminosity function
- `ResidualCalculator`: Helper class for fitting
- `residual_function()`: Creates residual functions for lmfit
- `fit_schechter_emcee()`: MCMC fitting with emcee
- `calculate_chi_squared()`: Goodness-of-fit statistics
- `get_confidence_intervals()`: MCMC confidence bands

#### `data_loader.py` (200 lines)
Data management utilities:
- `load_ha_database()`: Load CSV H-alpha data
- `load_excel_sheets()`: Load multi-sheet Excel files
- `prepare_redshift_bins()`: Organize data by redshift
- `extract_data_for_fitting()`: Prepare data for fitting
- `export_plotted_data()`: Export to CSV

#### `models.py` (250 lines)
Physical models and conversions:
- `convert_ha_to_radio()`: SFR-radio conversion
- `calculate_csfd()`: Cosmic SFR density calculation
- `madau_dickinson_2014()`: M&D14 CSFH model
- `create_hybrid_spline_fit()`: Multi-model spline fitting

#### `plotting.py` (300 lines)
Visualization functions:
- `darken_color()`: Color manipulation
- `plot_luminosity_functions()`: Multi-panel LF plots
- `plot_schechter_fit()`: Individual fits with CI
- `plot_csfd_evolution()`: CSFD vs redshift

### Data Files (`data/`)

#### `Ha_Database_20250501.xlsx` (112 KB)
Multi-sheet Excel file containing:
- 28 sheets from different surveys/studies
- Columns: redshift, luminosities, phi values, errors
- Schechter parameters
- CSFD compilation

#### `EMU_GAMA_20250902` (12 MB)
FITS format file with:
- EMU-GAMA radio survey data
- Used for testing and validation

### Tests (`tests/`)

#### `test_basic.py` (250 lines)
Tests core functionality:
- Data loading (Test 1)
- H-alpha to radio conversion (Test 2)
- Schechter fitting on synthetic data (Test 3)
- CSFD calculation (Test 4)

Expected runtime: ~2 minutes

#### `test_plotting.py` (200 lines)
Tests visualization:
- Luminosity function plotting
- CSFD evolution plotting
- Madau & Dickinson model

Expected runtime: ~1 minute

### Examples (`examples/`)

#### `complete_workflow.py` (300 lines)
Full analysis pipeline demonstrating:
1. Loading data from Excel
2. Converting H-alpha to radio
3. Plotting luminosity functions
4. Fitting Schechter functions (3 bins)
5. Calculating CSFD
6. Creating publication plots

Expected runtime: ~5-10 minutes
Outputs: 6 PNG files + 1 CSV file

### Configuration Files

#### `setup.py`
- Package metadata (name, version, author)
- Dependencies specification
- Entry points (if any)
- Classifiers for PyPI

#### `requirements.txt`
Core dependencies only:
- numpy>=1.20.0
- pandas>=1.3.0
- matplotlib>=3.4.0
- scipy>=1.7.0
- lmfit>=1.0.0
- emcee>=3.0.0
- corner>=2.2.0
- openpyxl>=3.0.0

#### `MANIFEST.in`
Specifies non-Python files to include in distribution:
- README.md, LICENSE
- Data files
- Documentation files

#### `.gitignore`
Excludes from version control:
- Python cache files (`__pycache__/`)
- Build artifacts (`dist/`, `build/`)
- Generated plots (`.png`, `.pdf`)
- Virtual environments (`venv/`)

### Documentation

#### `README.md` (800 lines)
Complete package documentation:
- Features overview
- Installation instructions
- Quick start examples
- Detailed usage for all functions
- Complete workflow example
- API reference
- Scientific background
- Citation information

#### `QUICKSTART.md` (150 lines)
5-minute introduction:
- Installation (1 command)
- Basic usage (6 examples)
- Common patterns
- Function reference table
- Quick troubleshooting

#### `INSTALL.md` (400 lines)
Detailed installation guide:
- Prerequisites
- Multiple installation methods
- Verification steps
- Platform-specific notes
- Troubleshooting common issues
- Development installation

#### `CONTRIBUTING.md` (500 lines)
Contribution guidelines:
- Code of conduct
- How to report bugs
- Feature requests
- Development setup
- Coding standards
- Testing guidelines
- PR process

#### `CHANGELOG.md`
Version history:
- What's new in each version
- Breaking changes
- Bug fixes
- Future plans

#### `LICENSE`
MIT License - permissive open source license

### Utilities

#### `verify_installation.py` (300 lines)
Comprehensive installation check:
- Python version
- Package import
- Dependencies
- Submodules
- Data files
- Core functions
- Quick functional test

## Module Dependencies

```
glumf (main package)
├── core
│   ├── numpy
│   ├── lmfit
│   ├── emcee
│   └── scipy.stats
├── data_loader
│   ├── pandas
│   └── numpy
├── models
│   ├── numpy
│   ├── pandas
│   ├── scipy.stats
│   └── scipy.interpolate
└── plotting
    ├── numpy
    ├── matplotlib
    ├── colorsys
    └── glumf.core
```

## Data Flow

```
Excel/CSV Files
      ↓
load_excel_sheets()
      ↓
Data Dictionary
      ↓
convert_ha_to_radio()
      ↓
Radio Luminosities
      ↓
plot_luminosity_functions()  →  plotted_data dict
      ↓
export_plotted_data()
      ↓
plotted_data.csv
      ↓
prepare_redshift_bins()
      ↓
extract_data_for_fitting()
      ↓
fit_schechter_emcee()
      ↓
Schechter Parameters
      ↓
calculate_csfd()
      ↓
CSFD Results
      ↓
plot_csfd_evolution()
      ↓
Publication Figure
```

## Typical Usage Flow

1. **Load data**: `load_excel_sheets()` → data dictionary
2. **Convert**: `convert_ha_to_radio()` → adds radio columns
3. **Visualize**: `plot_luminosity_functions()` → figures + plotted_data
4. **Export**: `export_plotted_data()` → CSV file
5. **Organize**: `prepare_redshift_bins()` → binned data
6. **Fit**: `fit_schechter_emcee()` → parameters + samples
7. **Calculate**: `calculate_csfd()` → CSFD values
8. **Plot**: `plot_csfd_evolution()` → final figure

## Code Statistics

| Component | Files | Lines | Functions |
|-----------|-------|-------|-----------|
| Core package | 4 | ~1100 | 20+ |
| Tests | 2 | ~450 | 8 |
| Examples | 1 | ~300 | 1 |
| Total Python | 7 | ~1850 | 30+ |
| Documentation | 6 | ~2500 | - |

## Size Information

| Item | Size |
|------|------|
| Package code | ~60 KB |
| Data files | ~12 MB |
| Documentation | ~100 KB |
| Total | ~12.2 MB |

## Version Control

Files tracked in git:
- All Python code
- All documentation
- Configuration files
- Data files (using Git LFS recommended for large files)

Files ignored (`.gitignore`):
- Python cache
- Build artifacts
- Generated plots
- Virtual environments
- IDE config files

## Building Distribution

```bash
# Build source distribution
python setup.py sdist

# Build wheel
python setup.py bdist_wheel

# Install from built package
pip install dist/glumf-1.0.0-py3-none-any.whl
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
python tests/test_basic.py

# Run with coverage
pytest --cov=glumf tests/

# Run verification
python verify_installation.py
```

## Documentation Generation

Documentation is in Markdown format. To convert to HTML/PDF:

```bash
# Using pandoc (if installed)
pandoc README.md -o README.html
pandoc README.md -o README.pdf

# Using grip (for GitHub-flavored Markdown)
grip README.md
```

## Future Structure Plans

Possible additions in future versions:
- `glumf/cli/` - Command-line interface
- `glumf/utils/` - Additional utilities
- `glumf/visualization/` - Advanced plotting (split from plotting.py)
- `docs/` - Sphinx documentation
- `.github/` - GitHub Actions CI/CD
- `notebooks/` - Jupyter notebook examples

## Notes

- Package follows standard Python package structure
- Code is modular and maintainable
- Comprehensive testing and documentation
- Ready for distribution via PyPI
- Follows semantic versioning
