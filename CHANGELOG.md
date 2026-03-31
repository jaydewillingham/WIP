# Changelog

All notable changes to the GLUMF package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-03-31

### Added
- Initial release of GLUMF package
- Core Schechter function fitting using emcee MCMC
- SFR to radio luminosity conversion functionality
- CSFD calculation from Schechter parameters
- Multi-redshift bin analysis tools
- Publication-quality plotting functions:
  - `plot_luminosity_functions()` for multi-panel LF plots
  - `plot_schechter_fit()` for individual fits with confidence intervals
  - `plot_csfd_evolution()` for CSFD vs redshift
- Data loading utilities:
  - `load_excel_sheets()` for multi-sheet Excel files
  - `prepare_redshift_bins()` for organizing data by redshift
  - `export_plotted_data()` for CSV export
- Statistical tools:
  - `calculate_chi_squared()` for goodness-of-fit
  - `get_confidence_intervals()` for MCMC confidence bands
- Complete documentation:
  - README.md with full API reference
  - INSTALL.md with detailed installation guide
  - QUICKSTART.md for rapid onboarding
- Example scripts:
  - `complete_workflow.py` demonstrating full analysis pipeline
- Test suite:
  - `test_basic.py` for core functionality
  - `test_plotting.py` for visualization tools
- Data files included:
  - Ha_Database_20250501.xlsx
  - EMU_GAMA_20250902 FITS file

### Features
- Support for asymmetric error bars in fitting
- Automatic color-coding of different datasets
- Integration with Madau & Dickinson 2014 CSFH model
- Flexible parameter bounds for Schechter fitting
- Progress bars for MCMC fitting
- Multiple output formats (PNG, PDF)

### Dependencies
- numpy >= 1.20.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0
- scipy >= 1.7.0
- lmfit >= 1.0.0
- emcee >= 3.0.0
- corner >= 2.2.0

## [Unreleased]

### Planned for v1.1.0
- Support for additional IMF conversions (Kroupa, Salpeter)
- Automated report generation
- Integration with astropy units
- Support for FITS table input
- Interactive plotting with plotly
- Command-line interface for common tasks
- Parallel processing for multiple redshift bins
- Additional luminosity function models (double power-law, Schechter+powerlaw)

### Under Consideration
- Web-based dashboard for interactive analysis
- Integration with online databases (NED, VizieR)
- Machine learning-based parameter initialization
- Bayesian model comparison tools
- Support for binned and unbinned likelihood fitting

## Notes

### Version Numbering
- Major version (X.y.z): Incompatible API changes
- Minor version (x.Y.z): New features, backwards compatible
- Patch version (x.y.Z): Bug fixes, backwards compatible

### Deprecation Policy
- Features marked as deprecated will be removed in the next major version
- Deprecation warnings will be issued for at least one minor version before removal
- Breaking changes will be clearly documented in this changelog
