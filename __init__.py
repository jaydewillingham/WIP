"""
GLUMF - Galaxy Luminosity Function Analysis Package
====================================================

A Python package for analyzing galaxy luminosity functions using Schechter function 
fitting with MCMC methods, SFR to radio luminosity conversions, and cosmic star 
formation rate density (CSFD) calculations.

Main Modules:
-------------
- core: Core Schechter function and fitting routines
- data_loader: Data loading and preprocessing utilities
- plotting: Plotting and visualization functions
- models: SFR conversion and CSFD calculation models

Author: [Your Name]
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "[Your Name]"

from .core import schechter, residual_function, fit_schechter_emcee, calculate_chi_squared
from .data_loader import load_ha_database, load_excel_sheets, prepare_redshift_bins
from .plotting import plot_luminosity_functions, plot_csfd_evolution, darken_color
from .models import convert_ha_to_radio, calculate_csfd

__all__ = [
    'schechter',
    'residual_function',
    'fit_schechter_emcee',
    'calculate_chi_squared',
    'load_ha_database',
    'load_excel_sheets',
    'prepare_redshift_bins',
    'plot_luminosity_functions',
    'plot_csfd_evolution',
    'darken_color',
    'convert_ha_to_radio',
    'calculate_csfd',
]
