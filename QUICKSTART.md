# GLUMF Quick Start Guide

A 5-minute guide to get started with GLUMF.

## Installation

```bash
cd glumf
pip install -e .
```

## Basic Usage

### 1. Load Data (10 seconds)

```python
from glumf import load_excel_sheets

data = load_excel_sheets('data/Ha_Database_20250501.xlsx')
```

### 2. Convert H-alpha to Radio (10 seconds)

```python
from glumf import convert_ha_to_radio

data = convert_ha_to_radio(data)
```

### 3. Plot Luminosity Functions (30 seconds)

```python
from glumf import plot_luminosity_functions

fig, axes, plotted_data = plot_luminosity_functions(
    data,
    output_path='lum_func.png'
)
```

### 4. Fit Schechter Function (1-2 minutes)

```python
from glumf import fit_schechter_emcee, extract_data_for_fitting
import pandas as pd

# Export and reload data
from glumf import export_plotted_data
export_plotted_data(plotted_data, 'plotted_data.csv')

df = pd.read_csv('plotted_data.csv')
df_bin = df[df['redshift_bin'] == '0-0.25']

all_x, all_y, all_yerr = extract_data_for_fitting(df_bin)

result = fit_schechter_emcee(all_x, all_y, all_yerr,
                              burn=300, steps=1000)

print(f"φ* = {result.params['phi'].value:.2e}")
print(f"L* = {result.params['Lstar'].value:.2e}")
print(f"α  = {result.params['a'].value:.3f}")
```

### 5. Calculate CSFD (1 second)

```python
from glumf import calculate_csfd

redshift_bins = {
    "bin1": [2e-4, 1e36, -1.5],
    "bin2": [1.5e-4, 8e35, -1.55],
}

csfd_results = calculate_csfd(redshift_bins)
print(csfd_results)
```

### 6. Plot CSFD Evolution (10 seconds)

```python
from glumf import plot_csfd_evolution

redshifts = [0.125, 0.375, 0.665]
log_CSFD = [-2.45, -2.46, -1.96]

fig = plot_csfd_evolution(
    redshifts, log_CSFD,
    output_path='csfd.png'
)
```

## Complete Example

Run the complete workflow:

```bash
cd examples
python complete_workflow.py
```

This generates:
- `luminosity_functions.png` - Multi-panel luminosity function plots
- `plotted_data.csv` - Extracted data in CSV format
- `schechter_fit_bin1.png`, etc. - Individual fits for each redshift bin
- `csfd_evolution.png` - CSFD vs redshift plot

## Common Patterns

### Pattern 1: Analyze Single Dataset

```python
from glumf import load_excel_sheets, convert_ha_to_radio

data = load_excel_sheets('my_data.xlsx')
data = convert_ha_to_radio(data)

# Access specific dataset
drake_data = data['Drake 2013']
print(drake_data[['Log_Rad_Lums_1', 'phi_Ha_undcorr_1']].head())
```

### Pattern 2: Fit Multiple Redshift Bins

```python
from glumf import fit_schechter_emcee
import pandas as pd

df = pd.read_csv('plotted_data.csv')
bins = df['redshift_bin'].unique()

results = {}
for bin_label in bins[:3]:  # First 3 bins
    df_bin = df[df['redshift_bin'] == bin_label]
    x, y, yerr = extract_data_for_fitting(df_bin)
    
    result = fit_schechter_emcee(x, y, yerr, 
                                  burn=200, steps=500, progress=False)
    results[bin_label] = result.params
```

### Pattern 3: Create Publication Plot

```python
from glumf import plot_csfd_evolution
import numpy as np

# Your data
z = np.array([0.125, 0.375, 0.665, 1.45, 3.0, 5.5])
csfd = np.array([-2.45, -2.46, -1.96, -1.50, -1.02, -1.58])

# Literature comparison
lit_data = {
    'covelo': ([0.4, 0.84, 1.47], [-2.10, -1.40, -1.15]),
}

# Create plot
fig = plot_csfd_evolution(
    z, csfd,
    literature_data=lit_data,
    figsize=(10, 6),
    output_path='figure1.pdf'
)
```

## Function Quick Reference

| Function | Purpose | Time |
|----------|---------|------|
| `load_excel_sheets()` | Load multi-sheet Excel data | 10s |
| `convert_ha_to_radio()` | Convert H-α to radio | 10s |
| `plot_luminosity_functions()` | Plot LF by redshift | 30s |
| `fit_schechter_emcee()` | Fit Schechter function | 1-5m |
| `calculate_csfd()` | Compute CSFD | <1s |
| `plot_csfd_evolution()` | Plot CSFD vs z | 10s |

## Testing Your Installation

```bash
# Quick test
python -c "import glumf; print(glumf.__version__)"

# Full test
cd tests
python test_basic.py
```

## Next Steps

1. ✅ Read full [README.md](README.md) for detailed API
2. ✅ Check [INSTALL.md](INSTALL.md) for troubleshooting
3. ✅ Run `examples/complete_workflow.py`
4. ✅ Explore your own data!

## Common Issues

**Import Error:**
```bash
pip install -e .  # Reinstall
```

**Missing Dependency:**
```bash
pip install -r requirements.txt
```

**Plot Not Showing:**
```python
import matplotlib
matplotlib.use('Agg')  # Add before glumf import
```

## Help

- Documentation: See README.md
- Examples: See examples/
- Issues: your.email@example.com

Happy analyzing! 🚀
