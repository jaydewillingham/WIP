"""
Models for SFR to radio luminosity conversion and CSFD calculations.

This module implements the conversion from H-alpha SFR to radio luminosities
and cosmic star formation rate density calculations.
"""

import numpy as np
import pandas as pd
from scipy.stats import gamma
import math


def convert_ha_to_radio(data_dict, a=0.55, b=0.22):
    """
    Convert H-alpha luminosities to radio luminosities for all datasets.
    
    This applies the SFR relationship to convert uncorrected H-alpha luminosities
    to radio continuum luminosities.
    
    Parameters
    ----------
    data_dict : dict
        Dictionary of DataFrames (from load_excel_sheets)
    a : float, optional
        Slope of SFR relationship line (default: 0.55)
    b : float, optional
        Intercept of SFR relationship line (default: 0.22)
        
    Returns
    -------
    dict
        Updated dictionary with radio luminosity columns added
    """
    luminosity_columns = [
        "log(L_Ha)_undcorr_1", "log(L_Ha)_undcorr_2",
        "log(L_Ha)_undcorr_3", "log(L_Ha)_undcorr_4"
    ]
    
    # Iterate through each DataFrame
    for sheet_name, df in data_dict.items():
        for i, col in enumerate(luminosity_columns, start=1):
            if col in df.columns:
                # Compute Ha_SFR_uncorr
                df[f"Ha_SFR_uncorr_{i}"] = (10**df[col]) * (7.9e-42) * (10**(-0.24))
                
                # Compute log10 of Ha_SFR_uncorr
                df[f"log_Ha_SFR_uncorr_{i}"] = np.log10(df[f"Ha_SFR_uncorr_{i}"])
                
                # Apply condition to Rad_SFRs
                df[f"Rad_SFRs_{i}"] = np.where(
                    df[f"log_Ha_SFR_uncorr_{i}"] <= -0.468085,
                    df[f"log_Ha_SFR_uncorr_{i}"],
                    (df[f"log_Ha_SFR_uncorr_{i}"] + b) / a
                )
                
                # Convert SFR_Rad to Radio Luminosities (originally in erg/s)
                df[f"Rad_Lums_{i}"] = (10**df[f"Rad_SFRs_{i}"]) / ((7.9e-42) * (10**(-0.24)))
                
                # Convert Radio Lums to be logged!
                df[f"Log_Rad_Lums_{i}"] = np.log10(df[f"Rad_Lums_{i}"])
        
        # Store back the modified DataFrame
        data_dict[sheet_name] = df
    
    return data_dict


def calculate_csfd(redshift_bins_params, Llim=37):
    """
    Calculate Cosmic Star Formation Rate Density from Schechter parameters.
    
    Parameters
    ----------
    redshift_bins_params : dict
        Dictionary mapping bin names to [phi, Lstar, alpha] lists
    Llim : float, optional
        Luminosity limit (default: 37)
        
    Returns
    -------
    dict
        Dictionary with log_CurlyL and log_CSFD for each bin
    """
    results = {}
    
    for name, (phi, Lstar, alpha) in redshift_bins_params.items():
        # Compute CurlyL using incomplete gamma function
        CurlyL = phi * (Lstar * 1e7) * gamma.cdf(alpha + 2, Llim / (Lstar * 1e7))
        log_CurlyL = round(np.log10(CurlyL), 4)
        
        # Compute CSFD with Chabrier correction
        CSFD = 7.9e-42 * CurlyL * (10**(-0.24))
        log_CSFD = round(np.log10(CSFD), 4)
        
        results[name] = {
            "log_CurlyL": log_CurlyL,
            "log_CSFD": log_CSFD
        }
    
    return results


def madau_dickinson_2014(z, imf_correction=True):
    """
    Madau & Dickinson (2014) cosmic star formation history.
    
    Parameters
    ----------
    z : array-like or float
        Redshift values
    imf_correction : bool, optional
        Apply Salpeter to Chabrier IMF correction (default: True)
        
    Returns
    -------
    array-like or float
        Star formation rate density in M_sun yr^-1 Mpc^-3
    """
    sfrd = 0.015 * (1 + z)**2.7 / (1 + ((1 + z) / 2.9)**5.6)
    if imf_correction:
        sfrd *= 0.63
    return sfrd


def create_hybrid_spline_fit(redshifts, case1_CSFD, case2_CSFD, case3_CSFD, log_CSFD_list,
                               z_break=3.7, z_target=13.0):
    """
    Create a hybrid spline fit combining multiple models.
    
    Parameters
    ----------
    redshifts : array-like
        Redshift values for model points
    case1_CSFD : array-like
        Model 1 CSFD values
    case2_CSFD : array-like
        Model 2 CSFD values
    case3_CSFD : array-like
        Model 3 CSFD values
    log_CSFD_list : array-like
        Model 4 CSFD values
    z_break : float, optional
        Redshift where spline transitions to linear
    z_target : float, optional
        Target redshift for linear extrapolation
        
    Returns
    -------
    dict
        Dictionary with 'z_full' and 'csfd_full' arrays
    """
    from scipy.interpolate import UnivariateSpline
    
    z_model = np.array(redshifts)
    model2 = np.array(case2_CSFD)
    model3 = np.array(case3_CSFD)
    model4 = np.array(log_CSFD_list)
    
    # Piecewise selection
    mask_m4 = z_model <= 0.7
    mask_m3 = (z_model > 0.7) & (z_model <= 1.5)
    mask_m2 = z_model > 1.5
    
    z_anchor = np.concatenate([
        z_model[mask_m4],
        z_model[mask_m3],
        z_model[mask_m2]
    ])
    
    csfd_anchor = np.concatenate([
        model4[mask_m4],
        model3[mask_m3],
        model2[mask_m2]
    ])
    
    # Sort
    order = np.argsort(z_anchor)
    z_anchor = z_anchor[order]
    csfd_anchor = csfd_anchor[order]
    
    # Force peak near 2nd M4 point
    weights = np.ones_like(z_anchor)
    z_peak_target = redshifts[1]
    peak_idx = np.argmin(np.abs(z_anchor - z_peak_target))
    weights[peak_idx] = 20.0
    
    # Smooth spline with weights
    spline = UnivariateSpline(z_anchor, csfd_anchor, w=weights, k=3, s=0.2)
    
    # Spline part
    z_spline_low = np.linspace(0, z_break, 500)
    csfd_spline_low = spline(z_spline_low)
    
    # Value at the break
    y_break = spline(z_break)
    
    # Extrapolate Model 1 to z_target
    z_m1 = np.array(redshifts)
    y_m1 = np.array(case1_CSFD)
    m1_slope = (y_m1[-1] - y_m1[-2]) / (z_m1[-1] - z_m1[-2])
    y_m1_target = y_m1[-1] + m1_slope * (z_target - z_m1[-1])
    
    # Linear tail
    z_linear = np.linspace(z_break, z_target, 300)
    csfd_linear = y_break + (y_m1_target - y_break) * (
        (z_linear - z_break) / (z_target - z_break)
    )
    
    # Combine
    z_full = np.concatenate([z_spline_low, z_linear])
    csfd_full = np.concatenate([csfd_spline_low, csfd_linear])
    
    return {
        'z_full': z_full,
        'csfd_full': csfd_full,
        'spline': spline,
        'z_anchor': z_anchor,
        'csfd_anchor': csfd_anchor
    }
