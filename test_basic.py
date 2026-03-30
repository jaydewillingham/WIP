"""
Test script for basic glumf functionality.

This script tests the core functions of the glumf package:
- Data loading
- Schechter function fitting
- CSFD calculations
"""

import numpy as np
import pandas as pd
import sys
import os

# Add parent directory to path for importing glumf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from glumf import (
    load_excel_sheets,
    convert_ha_to_radio,
    fit_schechter_emcee,
    calculate_chi_squared,
    extract_data_for_fitting,
    prepare_redshift_bins,
    export_plotted_data,
    calculate_csfd
)


def test_data_loading():
    """Test data loading from Excel file."""
    print("=" * 60)
    print("TEST 1: Data Loading")
    print("=" * 60)
    
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Ha_Database_20250501.xlsx')
    
    print(f"Loading data from: {data_path}")
    data = load_excel_sheets(data_path)
    
    print(f"✓ Loaded {len(data)} sheets")
    print(f"  Sheet names: {list(data.keys())[:5]}...")
    print(f"  First sheet shape: {data[list(data.keys())[0]].shape}")
    
    return data


def test_ha_to_radio_conversion(data):
    """Test H-alpha to radio conversion."""
    print("\n" + "=" * 60)
    print("TEST 2: H-alpha to Radio Conversion")
    print("=" * 60)
    
    print("Converting H-alpha luminosities to radio...")
    data_converted = convert_ha_to_radio(data)
    
    # Check if conversion columns were added
    first_sheet = list(data_converted.keys())[0]
    df = data_converted[first_sheet]
    
    radio_cols = [col for col in df.columns if 'Log_Rad_Lums' in col]
    print(f"✓ Added {len(radio_cols)} radio luminosity columns")
    print(f"  Columns: {radio_cols}")
    
    return data_converted


def test_schechter_fitting():
    """Test Schechter function fitting on synthetic data."""
    print("\n" + "=" * 60)
    print("TEST 3: Schechter Function Fitting")
    print("=" * 60)
    
    # Create synthetic data
    np.random.seed(42)
    true_phi = 1e-3
    true_Lstar = 1e41
    true_alpha = -1.5
    
    # Generate log luminosities
    log_L = np.linspace(38, 43, 20)
    L = 10**log_L
    
    from glumf.core import schechter
    
    # Generate data with noise
    phi_true = schechter(L, true_phi, true_Lstar, true_alpha)
    noise = np.random.normal(0, 0.1 * phi_true)
    phi_obs = phi_true + noise
    phi_err = 0.1 * phi_obs
    
    print("Synthetic data generated:")
    print(f"  True parameters: phi={true_phi:.2e}, L*={true_Lstar:.2e}, alpha={true_alpha}")
    print(f"  Data points: {len(log_L)}")
    
    # Fit
    print("\nFitting with emcee (this may take a minute)...")
    result = fit_schechter_emcee(
        log_L, phi_obs, phi_err,
        phi_init=1e-3, Lstar_init=1e41, alpha_init=-1.5,
        burn=100, steps=500, thin=10, progress=False
    )
    
    phi_fit = result.params['phi'].value
    Lstar_fit = result.params['Lstar'].value
    alpha_fit = result.params['a'].value
    
    print("\nFit results:")
    print(f"  phi_fit   = {phi_fit:.2e} (true: {true_phi:.2e})")
    print(f"  Lstar_fit = {Lstar_fit:.2e} (true: {true_Lstar:.2e})")
    print(f"  alpha_fit = {alpha_fit:.3f} (true: {true_alpha:.3f})")
    
    # Calculate chi-squared
    chi2_results = calculate_chi_squared(log_L, phi_obs, phi_err, phi_fit, Lstar_fit, alpha_fit)
    print(f"\n✓ Chi-squared: {chi2_results['chi_squared']:.2f}")
    print(f"  DOF: {chi2_results['dof']}")
    print(f"  Reduced chi-squared: {chi2_results['reduced_chi2']:.2f}")
    
    return result


def test_csfd_calculation():
    """Test CSFD calculation."""
    print("\n" + "=" * 60)
    print("TEST 4: CSFD Calculation")
    print("=" * 60)
    
    # Example redshift bins parameters
    redshift_bins = {
        "redbin1": [2e-4, 1e36, -1.5],
        "redbin2": [1.5e-4, 8e35, -1.55],
        "redbin3": [1e-4, 5e35, -1.6],
    }
    
    print("Calculating CSFD for example bins...")
    results = calculate_csfd(redshift_bins)
    
    print("\nResults:")
    for name, values in results.items():
        print(f"  {name}:")
        print(f"    log(CurlyL) = {values['log_CurlyL']}")
        print(f"    log(CSFD)   = {values['log_CSFD']}")
    
    print("\n✓ CSFD calculation successful")
    
    return results


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("GLUMF PACKAGE FUNCTIONALITY TESTS")
    print("=" * 60 + "\n")
    
    try:
        # Test 1: Data loading
        data = test_data_loading()
        
        # Test 2: Conversion
        data_converted = test_ha_to_radio_conversion(data)
        
        # Test 3: Fitting
        fit_result = test_schechter_fitting()
        
        # Test 4: CSFD
        csfd_results = test_csfd_calculation()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
