"""
Plotting and visualization functions.

This module provides functions for plotting luminosity functions,
CSFD evolution, and other visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
import colorsys
from matplotlib.colors import to_rgb


def darken_color(rgb, factor=0.9):
    """
    Darken a color by reducing its lightness.
    
    Parameters
    ----------
    rgb : tuple
        RGB color tuple (values 0-1)
    factor : float, optional
        Factor to darken (default: 0.9)
        
    Returns
    -------
    tuple
        Darkened RGB color
    """
    h, l, s = colorsys.rgb_to_hls(*rgb[:3])
    l = max(0, min(1, l * factor))
    return colorsys.hls_to_rgb(h, l, s)


def plot_luminosity_functions(data_dict, z_bins=None, figsize=(18, 12), output_path=None):
    """
    Plot luminosity functions for different redshift bins.
    
    Parameters
    ----------
    data_dict : dict
        Dictionary of DataFrames with luminosity data
    z_bins : list of tuples, optional
        Redshift bins as (z_min, z_max)
    figsize : tuple, optional
        Figure size
    output_path : str, optional
        Path to save the figure
        
    Returns
    -------
    tuple
        (fig, axes, plotted_data) where plotted_data is a dict
    """
    if z_bins is None:
        z_bins = [(0, 0.25), (0.26, 0.5), (0.51, 0.83), (0.84, 2), (2.1, 4), (4.01, 7)]
    
    # Define column pairs
    luminosity_columns = [f'Log_Rad_Lums_{i}' for i in range(1, 5)]
    phi_columns = [f'phi_Ha_undcorr_{i}' for i in range(1, 5)]
    phi_err_low_columns = [f"phi_Ha_undcorr_low_{i}" for i in range(1, 5)]
    phi_err_upp_columns = [f"phi_Ha_undcorr_upp_{i}" for i in range(1, 5)]
    z_columns = [f"z_{i}" for i in range(1, 5)]
    
    # Storage for plotted data
    plotted_data = {}
    
    # Create subplots
    fig, axes = plt.subplots(2, 3, figsize=figsize, sharex=True, sharey=True)
    axes = axes.flatten()
    
    # Iterate through redshift bins
    for bin_idx, (z_min, z_max) in enumerate(z_bins):
        ax = axes[bin_idx]
        handles_labels = {}
        z_bin_label = f"{z_min}-{z_max}"
        plotted_data[z_bin_label] = {}
        
        # Colormap
        cmap = plt.colormaps.get_cmap("gist_ncar")
        colors = [darken_color(cmap(i / (len(data_dict) - 1)), factor=0.6) 
                  for i in range(len(data_dict))]
        
        for idx, (sheet_name, df) in enumerate(data_dict.items()):
            color = colors[idx]
            
            for i in range(4):
                lum_col = luminosity_columns[i]
                phi_col = phi_columns[i]
                phi_low_col = phi_err_low_columns[i]
                phi_upp_col = phi_err_upp_columns[i]
                z_col = z_columns[i]
                
                if lum_col in df.columns and phi_col in df.columns and z_col in df.columns:
                    df_filtered = df[(df[z_col] >= z_min) & (df[z_col] < z_max)].copy()
                    
                    if not df_filtered.empty:
                        df_filtered[lum_col] = df_filtered[lum_col] - 7  # erg/s → W
                        
                        x = df_filtered[lum_col]
                        y = df_filtered[phi_col]
                        yerr_lower = -1 * df_filtered[phi_low_col]
                        yerr_upper = df_filtered[phi_upp_col]
                        yerr = [yerr_lower, yerr_upper]
                        
                        handle = ax.errorbar(
                            x, y, yerr=yerr, fmt='o', label=sheet_name, alpha=0.6,
                            markersize=5, color=color, capsize=3, capthick=1, elinewidth=1
                        )
                        
                        handles_labels[sheet_name] = handle
                        
                        if sheet_name not in plotted_data[z_bin_label]:
                            plotted_data[z_bin_label][sheet_name] = {
                                'x': [], 'y': [], 'yerr': ([], [])
                            }
                        
                        plotted_data[z_bin_label][sheet_name]['x'].extend(x.values)
                        plotted_data[z_bin_label][sheet_name]['y'].extend(y.values)
                        plotted_data[z_bin_label][sheet_name]['yerr'][0].extend(yerr_lower.values)
                        plotted_data[z_bin_label][sheet_name]['yerr'][1].extend(yerr_upper.values)
        
        ax.set_title(f"z: {z_min}-{z_max}", fontsize=20)
        ax.set_xlabel('Log(L$_{H\\alpha}$) (W)', fontsize=20)
        ax.set_ylabel('$\\phi(L)$ (Mpc$^{-3}$ dex$^{-1}$)', fontsize=20)
        ax.set_yscale("log")
        
        if handles_labels:
            ax.legend(list(handles_labels.values()), list(handles_labels.keys()), 
                     fontsize=12, loc="best", ncol=2)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    return fig, axes, plotted_data


def plot_schechter_fit(all_x, all_y, all_yerr, phi_best, Lstar_best, alpha_best, 
                        samples=None, z_bin_label=None, output_path=None):
    """
    Plot data with Schechter function fit and confidence intervals.
    
    Parameters
    ----------
    all_x : array-like
        Log luminosity values
    all_y : array-like
        Phi values
    all_yerr : array-like
        Phi errors
    phi_best, Lstar_best, alpha_best : float
        Best-fit parameters
    samples : object, optional
        MCMC samples for confidence intervals
    z_bin_label : str, optional
        Redshift bin label for title
    output_path : str, optional
        Path to save figure
        
    Returns
    -------
    matplotlib.figure.Figure
        The figure object
    """
    from .core import schechter, get_confidence_intervals
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot data with error bars
    datasets = np.unique([f"data_{i}" for i in range(len(all_x))])
    
    # For simplicity, plot all data in one color
    ax.errorbar(all_x, all_y, yerr=all_yerr, fmt='o', capsize=3,
                label='Data', color='blue', markersize=6, alpha=0.7)
    
    # Generate fit line
    log_L_fit = np.linspace(np.min(all_x) - 2, np.max(all_x) + 2, 300)
    L_fit = 10 ** log_L_fit
    schechter_best = schechter(L_fit, phi_best, Lstar_best, alpha_best)
    
    # Plot best fit
    ax.plot(log_L_fit, schechter_best, label='Best Fit', color='black', linewidth=2)
    
    # Add confidence intervals if samples provided
    if samples is not None:
        ci = get_confidence_intervals(samples, L_fit)
        ax.fill_between(log_L_fit, ci['lower_bound'], ci['upper_bound'], 
                        color='gray', alpha=0.4, label='95% CI')
    
    ax.set_yscale('log')
    ax.set_xlabel('Log(L$_{H\\alpha}$) [W]', fontsize=14)
    ax.set_ylabel('$\\phi(L)$ [Mpc$^{-3}$ dex$^{-1}$]', fontsize=14)
    
    if z_bin_label:
        ax.set_title(f'Schechter Fit for Redshift Bin: {z_bin_label}', fontsize=16)
    else:
        ax.set_title('Schechter Function Fit', fontsize=16)
    
    ax.legend()
    ax.set_ylim(1e-8, 1)
    ax.set_xlim(30, 44)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_csfd_evolution(redshifts, log_CSFD_list, csfd_data=None, 
                         literature_data=None, figsize=(10, 6), output_path=None):
    """
    Plot cosmic star formation rate density evolution.
    
    Parameters
    ----------
    redshifts : array-like
        Redshift values for this work
    log_CSFD_list : array-like
        Log CSFD values for this work
    csfd_data : pandas.DataFrame, optional
        Observational CSFD data with columns: wavelength, z mid, log(csfd), csfd_err_low, csfd_err_upp
    literature_data : dict, optional
        Dictionary with 'covelo', 'chiang', etc. keys containing (z, csfd) tuples
    figsize : tuple, optional
        Figure size
    output_path : str, optional
        Path to save figure
        
    Returns
    -------
    matplotlib.figure.Figure
        The figure object
    """
    from .models import madau_dickinson_2014
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot observational data if provided
    if csfd_data is not None:
        wavelength_types = csfd_data['wavelength'].unique()
        markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X']
        grey_values = np.linspace(0.3, 0.8, len(wavelength_types))
        colors = [(v, v, v) for v in grey_values]
        
        for i, w in enumerate(wavelength_types):
            subset = csfd_data[csfd_data['wavelength'] == w]
            yerr = [-1 * subset['csfd_err_low'], subset['csfd_err_upp']]
            ax.errorbar(
                subset['z mid'], subset['log(csfd) '],
                yerr=yerr,
                fmt=markers[i % len(markers)],
                capsize=3, alpha=0.85, markersize=8,
                linestyle='none', color=colors[i % len(colors)]
            )
    
    # Plot this work
    ax.plot(redshifts, log_CSFD_list, 'D--', label="This Work", 
            color='mediumvioletred', linewidth=3, markersize=8)
    
    # Plot literature data if provided
    if literature_data:
        if 'covelo' in literature_data:
            zs, csfds = literature_data['covelo']
            ax.plot(zs, csfds, 'X--', label="Covelo+24", 
                   linewidth=3, color='darkgrey', markersize=10)
        
        if 'chiang' in literature_data:
            zs, csfds = literature_data['chiang']
            ax.plot(zs, csfds, 'P-.', label="Chiang+25", 
                   color='silver', linewidth=3, markersize=10)
    
    # Plot Madau & Dickinson 2014
    z_grid = np.linspace(0.3, 6, 300)
    log_sfrd_md14 = np.log10(madau_dickinson_2014(z_grid))
    ax.plot(z_grid, log_sfrd_md14, color="grey", linestyle="-", 
           linewidth=3, label="Madau & Dickinson 2014")
    
    ax.set_xlim(0, 6)
    ax.set_ylim(-2.75, -0.3)
    ax.set_xlabel("Redshift", fontsize=16, fontweight='bold')
    ax.set_ylabel(r"log$_{10}$($\rho_{\rm SFR}$) [M$_\odot$ yr$^{-1}$ Mpc$^{-3}$]", 
                 fontsize=14, fontweight='bold')
    
    ax.tick_params(axis='both', which='major', labelsize=12, width=2)
    ax.tick_params(axis='both', which='minor', width=2)
    ax.minorticks_on()
    for spine in ax.spines.values():
        spine.set_linewidth(2)
    
    ax.legend(fontsize=12, title_fontsize=13, loc='upper left')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=1200, bbox_inches='tight')
    
    return fig
