# GLUMF - Galaxy Luminosity Function Analysis Package

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive Python package for analyzing galaxy luminosity functions using Schechter function fitting with MCMC methods, converting star formation rates (SFR) to radio continuum luminosities, and calculating cosmic star formation rate density (CSFD) evolution.

## Features

- **Schechter Function Fitting**: Robust MCMC-based fitting using `emcee` and `lmfit`
- **SFR-Radio Conversion**: Convert H-alpha SFR to radio continuum luminosities
- **CSFD Calculations**: Compute cosmic star formation rate density across redshift
- **Multi-Redshift Analysis**: Analyze luminosity functions across different redshift bins
- **Publication-Quality Plots**: Generate publication-ready figures with customizable styling
- **Data Management**: Efficient loading and preprocessing of multi-sheet Excel databases

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/glumf.git
cd glumf

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Dependencies

The package requires the following Python packages:
- `numpy >= 1.20.0`
- `pandas >= 1.3.0`
- `matplotlib >= 3.4.0`
- `scipy >= 1.7.0`
- `lmfit >= 1.0.0`
- `emcee >= 3.0.0`
- `corner >= 2.2.0`

## Quick Start

```python
import glumf
from glumf import load_excel_sheets, convert_ha_to_radio, fit_schechter_emcee

# Load your H-alpha database
data = load_excel_sheets('path/to/Ha_Database.xlsx')

# Convert H-alpha to radio luminosities
data = convert_ha_to_radio(data, a=0.55, b=0.22)

# Fit Schechter function to your data
result = fit_schechter_emcee(
    log_L, phi, phi_err,
    phi_init=2e-4,
    Lstar_init=1e36,
    alpha_init=-1.5,
    burn=300,
    steps=1000
)

print(f"Best-fit parameters:")
print(f"  φ* = {result.params['phi'].value:.2e}")
print(f"  L* = {result.params['Lstar'].value:.2e}")
print(f"  α  = {result.params['a'].value:.3f}")
```

## Detailed Usage

### 1. Data Loading

```python
from glumf import load_excel_sheets

# Load all sheets from Excel file
data = load_excel_sheets('Ha_Database_20250501.xlsx')

# Access individual datasets
drake_data = data['Drake 2013']
sobral_data = data['Sobral 2013']
```

### 2. SFR to Radio Conversion

The package implements the conversion from H-alpha SFR to radio continuum luminosities:

```python
from glumf import convert_ha_to_radio

# Convert with default parameters (a=0.55, b=0.22)
data = convert_ha_to_radio(data)

# Or specify custom parameters
data = convert_ha_to_radio(data, a=0.6, b=0.2)
```

This adds columns like `Log_Rad_Lums_1`, `Log_Rad_Lums_2`, etc. to each dataset.

### 3. Plotting Luminosity Functions

```python
from glumf import plot_luminosity_functions

# Define redshift bins
z_bins = [(0, 0.25), (0.26, 0.5), (0.51, 0.83), (0.84, 2), (2.1, 4), (4.01, 7)]

# Create multi-panel plot
fig, axes, plotted_data = plot_luminosity_functions(
    data,
    z_bins=z_bins,
    figsize=(18, 12),
    output_path='luminosity_functions.png'
)
```

### 4. Fitting Schechter Functions

```python
from glumf import fit_schechter_emcee, calculate_chi_squared, get_confidence_intervals

# Prepare your data
all_x = [...]  # log luminosities
all_y = [...]  # phi values
all_yerr = [...] # phi errors

# Fit using MCMC
result = fit_schechter_emcee(
    all_x, all_y, all_yerr,
    phi_init=2e-4,      # Initial φ*
    phi_min=1e-7,       # Minimum φ*
    phi_max=0.1,        # Maximum φ*
    Lstar_init=1e36,    # Initial L*
    Lstar_min=1e30,     # Minimum L*
    Lstar_max=1e37,     # Maximum L*
    alpha_init=-1.5,    # Initial α
    alpha_min=-2,       # Minimum α
    alpha_max=-1,       # Maximum α
    burn=300,           # Burn-in steps
    steps=1000,         # MCMC steps
    thin=20,            # Thinning
    progress=True       # Show progress bar
)

# Extract best-fit parameters
phi_best = result.params['phi'].value
Lstar_best = result.params['Lstar'].value
alpha_best = result.params['a'].value

# Calculate goodness of fit
chi2_results = calculate_chi_squared(
    all_x, all_y, all_yerr,
    phi_best, Lstar_best, alpha_best
)
print(f"Reduced χ² = {chi2_results['reduced_chi2']:.2f}")

# Get confidence intervals
L_fit = 10**np.linspace(38, 43, 300)
ci = get_confidence_intervals(result.flatchain, L_fit)
lower_bound = ci['lower_bound']
upper_bound = ci['upper_bound']
```

### 5. CSFD Calculations

```python
from glumf import calculate_csfd

# Define Schechter parameters for each redshift bin
redshift_bins = {
    "redbin1": [phi1, Lstar1, alpha1],
    "redbin2": [phi2, Lstar2, alpha2],
    "redbin3": [phi3, Lstar3, alpha3],
    # ...
}

# Calculate CSFD
csfd_results = calculate_csfd(redshift_bins, Llim=37)

# Extract CSFD values
for bin_name, values in csfd_results.items():
    print(f"{bin_name}:")
    print(f"  log(L_total) = {values['log_CurlyL']}")
    print(f"  log(CSFD)    = {values['log_CSFD']}")
```

### 6. Plotting CSFD Evolution

```python
from glumf import plot_csfd_evolution

# Your fitted CSFD values
redshifts = [0.125, 0.375, 0.665, 1.45, 3.0, 5.5]
log_CSFD_list = [-2.45, -2.46, -1.96, -1.50, -1.02, -1.58]

# Literature comparison data
literature_data = {
    'covelo': (
        [0.4, 0.84, 1.47, 2.23, 4.45, 5.3, 6.15],
        [-2.10, -1.40, -1.15, -0.89, -1.38, -1.54, -1.85]
    ),
    'chiang': (
        [0.5, 1.005, 2.002, 3.003, 4.002, 5.00],
        [-1.48, -1.19, -1.01, -1.22, -1.45, -1.65]
    )
}

# Create plot
fig = plot_csfd_evolution(
    redshifts,
    log_CSFD_list,
    literature_data=literature_data,
    figsize=(10, 6),
    output_path='csfd_evolution.pdf'
)
```

## Complete Workflow Example

See `examples/complete_workflow.py` for a full end-to-end example that:
1. Loads H-alpha database
2. Converts to radio luminosities
3. Plots luminosity functions
4. Fits Schechter functions for multiple redshift bins
5. Calculates CSFD evolution
6. Creates publication-quality plots

Run it with:
```bash
cd examples
python complete_workflow.py
```

## Testing

The package includes comprehensive tests:

```bash
# Run basic functionality tests
cd tests
python test_basic.py

# Run all tests with pytest (if installed)
pytest tests/
```

## Data Format

### Input Excel File Structure

The Excel file should contain multiple sheets, each representing a different survey or dataset. Required columns include:

- `z_1`, `z_2`, `z_3`, `z_4`: Redshift values
- `log(L_Ha)_undcorr_1`, `log(L_Ha)_undcorr_2`, ...: Uncorrected H-alpha luminosities
- `phi_Ha_undcorr_1`, `phi_Ha_undcorr_2`, ...: Phi values
- `phi_Ha_undcorr_low_1`, `phi_Ha_undcorr_upp_1`, ...: Error bars

### Output CSV Format

The `plotted_data.csv` file contains:
- `redshift_bin`: Redshift bin label (e.g., "0-0.25")
- `dataset`: Survey name
- `log_L_Ha_W`: Log luminosity in Watts
- `phi_L`: Luminosity function value
- `phi_err_low`, `phi_err_up`: Asymmetric error bars

## API Reference

### Core Functions

#### `schechter(L, phi_star, L_star, alpha)`
Compute the Schechter luminosity function.

**Parameters:**
- `L`: Luminosity values (array-like)
- `phi_star`: Normalization parameter
- `L_star`: Characteristic luminosity
- `alpha`: Faint-end slope

**Returns:** Schechter function values

#### `fit_schechter_emcee(...)`
Fit Schechter function using emcee MCMC.

**Returns:** `lmfit.MinimizerResult` with fitted parameters and MCMC samples

#### `calculate_chi_squared(all_x, all_y, all_yerr, phi_best, Lstar_best, alpha_best)`
Calculate chi-squared statistics.

**Returns:** Dictionary with `chi_squared`, `dof`, and `reduced_chi2`

### Data Loading

#### `load_excel_sheets(excel_path, sheets_to_load=None)`
Load multiple sheets from Excel file.

**Returns:** Dictionary mapping sheet names to DataFrames

#### `prepare_redshift_bins(df, z_bins=None)`
Organize data by redshift bins.

**Returns:** Dictionary of binned DataFrames

### Models

#### `convert_ha_to_radio(data_dict, a=0.55, b=0.22)`
Convert H-alpha SFR to radio luminosities.

**Returns:** Updated data dictionary

#### `calculate_csfd(redshift_bins_params, Llim=37)`
Calculate cosmic star formation rate density.

**Returns:** Dictionary with CSFD values for each bin

### Plotting

#### `plot_luminosity_functions(data_dict, z_bins=None, ...)`
Plot luminosity functions across redshift bins.

**Returns:** `(fig, axes, plotted_data)` tuple

#### `plot_csfd_evolution(redshifts, log_CSFD_list, ...)`
Plot CSFD vs redshift evolution.

**Returns:** Figure object

## Scientific Background

### Schechter Function

The Schechter function describes the galaxy luminosity function:

```
φ(L) dL = φ* (L/L*)^α exp(-L/L*) d(L/L*)
```

where:
- φ*: Normalization (number density at L*)
- L*: Characteristic luminosity
- α: Faint-end slope

### SFR-Radio Conversion

The conversion from H-alpha star formation rate to radio continuum luminosity follows:

```
log(SFR_radio) = log(SFR_Ha) if log(SFR_Ha) ≤ threshold
log(SFR_radio) = (log(SFR_Ha) + b) / a otherwise
```

### CSFD Calculation

Cosmic star formation rate density is calculated by integrating the luminosity function:

```
CSFD = ∫ φ(L) × SFR(L) dL
```

using the incomplete gamma function for numerical stability.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{glumf2025,
  author = {Your Name},
  title = {GLUMF: Galaxy Luminosity Function Analysis Package},
  year = {2025},
  url = {https://github.com/yourusername/glumf}
}
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on analysis methods from [Your Paper/Thesis]
- Uses emcee for MCMC sampling (Foreman-Mackey et al. 2013)
- Built with lmfit for parameter optimization

## Contact

Your Name - your.email@example.com

Project Link: https://github.com/yourusername/glumf

## Changelog

### Version 1.0.0 (2025-01-XX)
- Initial release
- Core Schechter fitting functionality
- SFR-radio conversion
- CSFD calculations
- Comprehensive plotting tools
- Full documentation and examples
