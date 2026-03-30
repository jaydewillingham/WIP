"""
Complete workflow example using glumf package.

This script demonstrates the full workflow from the original notebook:
1. Load data from Excel
2. Convert H-alpha to radio luminosities
3. Plot luminosity functions
4. Fit Schechter functions for each redshift bin
5. Calculate CSFD evolution
6. Create publication-quality plots
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
    prepare_redshift_bins,
    extract_data_for_fitting,
    fit_schechter_emcee,
    calculate_chi_squared,
    plot_schechter_fit,
    calculate_csfd,
    plot_csfd_evolution
)


def main():
    """Run the complete workflow."""
    
    print("=" * 70)
    print("GLUMF COMPLETE WORKFLOW EXAMPLE")
    print("=" * 70)
    
    # ========================================
    # STEP 1: Load data
    # ========================================
    print("\nSTEP 1: Loading data...")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Ha_Database_20250501.xlsx')
    data = load_excel_sheets(data_path)
    print(f"✓ Loaded {len(data)} datasets")
    
    # ========================================
    # STEP 2: Convert H-alpha to radio
    # ========================================
    print("\nSTEP 2: Converting H-alpha to radio luminosities...")
    data = convert_ha_to_radio(data, a=0.55, b=0.22)
    print("✓ Conversion complete")
    
    # ========================================
    # STEP 3: Plot luminosity functions
    # ========================================
    print("\nSTEP 3: Plotting luminosity functions by redshift...")
    z_bins = [(0, 0.25), (0.26, 0.5), (0.51, 0.83), (0.84, 2), (2.1, 4), (4.01, 7)]
    
    fig, axes, plotted_data = plot_luminosity_functions(
        data, 
        z_bins=z_bins,
        output_path='luminosity_functions.png'
    )
    print("✓ Luminosity function plot saved as 'luminosity_functions.png'")
    plt.close(fig)
    
    # ========================================
    # STEP 4: Export plotted data
    # ========================================
    print("\nSTEP 4: Exporting plotted data to CSV...")
    df_export = export_plotted_data(plotted_data, output_path='plotted_data.csv')
    print(f"✓ Exported {len(df_export)} data points to 'plotted_data.csv'")
    
    # ========================================
    # STEP 5: Fit Schechter functions
    # ========================================
    print("\nSTEP 5: Fitting Schechter functions for each redshift bin...")
    
    # Load the exported data
    df = pd.read_csv('plotted_data.csv')
    bin_data = prepare_redshift_bins(df, z_bins)
    
    # Storage for fit results
    fit_results = {}
    redshift_centers = []
    
    # Fit each bin (we'll do just the first 3 for speed in this example)
    bins_to_fit = list(bin_data.keys())[:3]
    
    for i, bin_label in enumerate(bins_to_fit):
        print(f"\n  Fitting bin {bin_label}...")
        
        df_bin = bin_data[bin_label]
        all_x, all_y, all_yerr = extract_data_for_fitting(df_bin)
        
        # Fit with emcee
        result = fit_schechter_emcee(
            all_x, all_y, all_yerr,
            phi_init=2e-4 if i == 0 else 2e-3,
            Lstar_init=10**36,
            alpha_init=-1.5,
            burn=150,  # Reduced for speed
            steps=500,
            thin=10,
            progress=False
        )
        
        phi_best = result.params['phi'].value
        Lstar_best = result.params['Lstar'].value
        alpha_best = result.params['a'].value
        
        print(f"    phi = {phi_best:.2e}, L* = {Lstar_best:.2e}, alpha = {alpha_best:.3f}")
        
        # Calculate chi-squared
        chi2 = calculate_chi_squared(all_x, all_y, all_yerr, phi_best, Lstar_best, alpha_best)
        print(f"    Reduced χ² = {chi2['reduced_chi2']:.2f}")
        
        # Plot individual fit
        fig = plot_schechter_fit(
            all_x, all_y, all_yerr, 
            phi_best, Lstar_best, alpha_best,
            samples=result.flatchain,
            z_bin_label=bin_label,
            output_path=f'schechter_fit_bin{i+1}.png'
        )
        print(f"    ✓ Saved fit plot as 'schechter_fit_bin{i+1}.png'")
        plt.close(fig)
        
        # Store results
        fit_results[f"redbin{i+1}"] = [phi_best, Lstar_best, alpha_best]
        
        # Get redshift center for plotting
        z_parts = bin_label.split('-')
        z_center = (float(z_parts[0]) + float(z_parts[1])) / 2
        redshift_centers.append(z_center)
    
    print("\n✓ All Schechter fits complete")
    
    # ========================================
    # STEP 6: Calculate CSFD
    # ========================================
    print("\nSTEP 6: Calculating Cosmic Star Formation Rate Density...")
    
    csfd_results = calculate_csfd(fit_results, Llim=37)
    
    log_CSFD_list = [csfd_results[f"redbin{i+1}"]["log_CSFD"] for i in range(len(fit_results))]
    
    print("\nCSFD Results:")
    for i, (name, values) in enumerate(csfd_results.items()):
        print(f"  {name} (z~{redshift_centers[i]:.2f}):")
        print(f"    log(CSFD) = {values['log_CSFD']}")
    
    # ========================================
    # STEP 7: Plot CSFD evolution
    # ========================================
    print("\nSTEP 7: Plotting CSFD evolution...")
    
    # Load CSFD data if available in the Excel file
    try:
        csfd_data = data['CSFD']
    except:
        csfd_data = None
    
    # Literature data
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
    
    fig = plot_csfd_evolution(
        redshift_centers,
        log_CSFD_list,
        csfd_data=csfd_data,
        literature_data=literature_data,
        output_path='csfd_evolution.png'
    )
    print("✓ CSFD evolution plot saved as 'csfd_evolution.png'")
    plt.close(fig)
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - luminosity_functions.png")
    print("  - plotted_data.csv")
    for i in range(len(fit_results)):
        print(f"  - schechter_fit_bin{i+1}.png")
    print("  - csfd_evolution.png")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
