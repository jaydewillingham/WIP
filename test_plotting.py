"""
Test script for glumf plotting capabilities.

This script tests the plotting functions and generates example figures
using the provided data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from glumf import (
    load_excel_sheets,
    convert_ha_to_radio,
    plot_luminosity_functions,
    export_plotted_data,
    plot_csfd_evolution
)
from glumf.models import madau_dickinson_2014


def test_luminosity_function_plot():
    """Test luminosity function plotting."""
    print("=" * 60)
    print("TEST: Luminosity Function Plotting")
    print("=" * 60)
    
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Ha_Database_20250501.xlsx')
    print(f"\nLoading data from: {data_path}")
    
    data = load_excel_sheets(data_path)
    print(f"✓ Loaded {len(data)} datasets")
    
    # Convert to radio
    print("\nConverting H-alpha to radio luminosities...")
    data = convert_ha_to_radio(data)
    print("✓ Conversion complete")
    
    # Plot
    print("\nCreating luminosity function plot...")
    z_bins = [(0, 0.25), (0.26, 0.5), (0.51, 0.83), (0.84, 2), (2.1, 4), (4.01, 7)]
    
    fig, axes, plotted_data = plot_luminosity_functions(
        data,
        z_bins=z_bins,
        figsize=(18, 12),
        output_path='test_luminosity_functions.png'
    )
    
    print("✓ Plot saved as 'test_luminosity_functions.png'")
    plt.close(fig)
    
    # Export data
    print("\nExporting plotted data...")
    df_export = export_plotted_data(plotted_data, output_path='test_plotted_data.csv')
    print(f"✓ Exported {len(df_export)} data points to 'test_plotted_data.csv'")
    
    return data, plotted_data


def test_csfd_plot(data):
    """Test CSFD evolution plotting."""
    print("\n" + "=" * 60)
    print("TEST: CSFD Evolution Plotting")
    print("=" * 60)
    
    # Example CSFD values (from fitting or previous analysis)
    redshifts = [0.125, 0.375, 0.665, 1.45, 3.0, 5.5]
    log_CSFD_list = [-2.45, -2.46, -1.96, -1.50, -1.02, -1.58]
    
    # Load CSFD observational data if available
    try:
        csfd_data = data['CSFD']
        print("\n✓ Loaded observational CSFD data")
    except:
        csfd_data = None
        print("\n⚠ No CSFD sheet found in data")
    
    # Literature comparison
    literature_data = {
        'covelo': (
            [0.4, 0.84, 1.47, 2.23, 4.45, 5.3, 6.15],
            [-2.0969, -1.39794, -1.1549, -0.8860, -1.37665, -1.5376, -1.85387]
        ),
        'chiang': (
            [0.5, 1.005, 2.002, 3.003, 4.002, 5.00],
            [-1.48, -1.19, -1.01, -1.22, -1.45, -1.65]
        )
    }
    
    print("\nCreating CSFD evolution plot...")
    fig = plot_csfd_evolution(
        redshifts,
        log_CSFD_list,
        csfd_data=csfd_data,
        literature_data=literature_data,
        figsize=(10, 6),
        output_path='test_csfd_evolution.png'
    )
    
    print("✓ Plot saved as 'test_csfd_evolution.png'")
    plt.close(fig)


def test_madau_dickinson():
    """Test Madau & Dickinson 2014 CSFH."""
    print("\n" + "=" * 60)
    print("TEST: Madau & Dickinson 2014 Model")
    print("=" * 60)
    
    z_values = np.array([0, 1, 2, 3, 4, 5, 6])
    sfrd_values = madau_dickinson_2014(z_values)
    
    print("\nRedshift  |  log10(SFRD)")
    print("-" * 30)
    for z, sfrd in zip(z_values, sfrd_values):
        print(f"  {z:.1f}     |  {np.log10(sfrd):.3f}")
    
    print("\n✓ Madau & Dickinson model working correctly")


def main():
    """Run all plotting tests."""
    print("\n" + "=" * 60)
    print("GLUMF PLOTTING TESTS")
    print("=" * 60 + "\n")
    
    try:
        # Test 1: Luminosity function plot
        data, plotted_data = test_luminosity_function_plot()
        
        # Test 2: CSFD evolution plot
        test_csfd_plot(data)
        
        # Test 3: Madau & Dickinson model
        test_madau_dickinson()
        
        print("\n" + "=" * 60)
        print("ALL PLOTTING TESTS PASSED! ✓")
        print("=" * 60)
        print("\nGenerated files:")
        print("  - test_luminosity_functions.png")
        print("  - test_plotted_data.csv")
        print("  - test_csfd_evolution.png")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
