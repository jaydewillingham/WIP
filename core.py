"""
Core functions for Schechter luminosity function fitting.

This module provides the fundamental Schechter function, residual calculations,
and MCMC fitting routines using emcee and lmfit.
"""

import numpy as np
import lmfit
from scipy.stats import chi2


def schechter(L, phi_star, L_star, alpha):
    """
    Schechter luminosity function.
    
    Parameters
    ----------
    L : array-like
        Luminosity values
    phi_star : float
        Normalization parameter
    L_star : float
        Characteristic luminosity
    alpha : float
        Faint-end slope
        
    Returns
    -------
    array-like
        Schechter function values
    """
    LOverLStar = L / L_star
    return (phi_star) * ((L / L_star) ** alpha) * np.exp(-L / L_star) * (L / L_star) * np.log(10)


class ResidualCalculator:
    """
    Helper class to calculate residuals for Schechter function fitting.
    """
    
    def __init__(self, all_x, all_y, all_yerr):
        """
        Initialize with data.
        
        Parameters
        ----------
        all_x : array-like
            Log luminosity values
        all_y : array-like
            Phi values
        all_yerr : array-like
            Phi error values
        """
        self.all_x = np.array(all_x)
        self.all_y = np.array(all_y)
        self.all_yerr = np.array(all_yerr)
    
    def residual(self, p):
        """
        Calculate weighted residuals for lmfit.
        
        Parameters
        ----------
        p : lmfit.Parameters
            Parameter object with 'phi', 'Lstar', and 'a'
            
        Returns
        -------
        array-like
            Weighted residuals
        """
        v = p.valuesdict()
        LOverL = 10**self.all_x / v['Lstar']
        model = v['phi'] * (LOverL ** v['a']) * np.exp(-LOverL) * LOverL * np.log(10)
        weights = self.all_yerr / (self.all_y * np.log(10))
        res = (np.log10(model) - np.log10(self.all_y)) / weights
        return res


def residual_function(all_x, all_y, all_yerr):
    """
    Create a residual function for use with lmfit.
    
    Parameters
    ----------
    all_x : array-like
        Log luminosity values
    all_y : array-like
        Phi values
    all_yerr : array-like
        Phi error values
        
    Returns
    -------
    callable
        Residual function
    """
    calculator = ResidualCalculator(all_x, all_y, all_yerr)
    return calculator.residual


def fit_schechter_emcee(all_x, all_y, all_yerr, 
                         phi_init=2e-4, phi_min=1e-7, phi_max=0.1,
                         Lstar_init=1e36, Lstar_min=1e30, Lstar_max=1e37,
                         alpha_init=-1.5, alpha_min=-2, alpha_max=-1,
                         burn=300, steps=1000, thin=20, progress=True):
    """
    Fit Schechter function using emcee MCMC.
    
    Parameters
    ----------
    all_x : array-like
        Log luminosity values
    all_y : array-like
        Phi values
    all_yerr : array-like
        Phi error values
    phi_init : float, optional
        Initial guess for phi_star
    phi_min, phi_max : float, optional
        Bounds for phi_star
    Lstar_init : float, optional
        Initial guess for L_star
    Lstar_min, Lstar_max : float, optional
        Bounds for L_star
    alpha_init : float, optional
        Initial guess for alpha
    alpha_min, alpha_max : float, optional
        Bounds for alpha
    burn : int, optional
        Burn-in steps for emcee
    steps : int, optional
        MCMC steps
    thin : int, optional
        Thinning factor
    progress : bool, optional
        Show progress bar
        
    Returns
    -------
    lmfit.MinimizerResult
        Result object containing fitted parameters and samples
    """
    # Define fit parameters
    p = lmfit.Parameters()
    p.add('phi', value=phi_init, min=phi_min, max=phi_max)
    p.add('Lstar', value=Lstar_init, min=Lstar_min, max=Lstar_max)
    p.add('a', value=alpha_init, min=alpha_min, max=alpha_max)
    
    # Create residual function
    residual_func = residual_function(all_x, all_y, all_yerr)
    
    # Run MCMC fit
    mi = lmfit.minimize(
        residual_func, 
        p, 
        method='emcee', 
        nan_policy='omit', 
        burn=burn, 
        steps=steps, 
        thin=thin, 
        is_weighted=True, 
        progress=progress
    )
    
    return mi


def calculate_chi_squared(all_x, all_y, all_yerr, phi_best, Lstar_best, alpha_best):
    """
    Calculate chi-squared and reduced chi-squared for the fit.
    
    Parameters
    ----------
    all_x : array-like
        Log luminosity values
    all_y : array-like
        Phi values
    all_yerr : array-like
        Phi error values
    phi_best : float
        Best-fit phi_star
    Lstar_best : float
        Best-fit L_star
    alpha_best : float
        Best-fit alpha
        
    Returns
    -------
    dict
        Dictionary with 'chi_squared', 'dof', and 'reduced_chi2'
    """
    # Convert to numpy arrays
    all_x = np.array(all_x)
    all_y = np.array(all_y)
    all_yerr = np.array(all_yerr)
    
    # Replace zero or negative errors with small positive value
    min_error = 1e-10
    all_yerr[all_yerr <= 0] = min_error
    
    # Remove any NaNs from data
    valid_mask = np.isfinite(all_x) & np.isfinite(all_y) & np.isfinite(all_yerr)
    all_x = all_x[valid_mask]
    all_y = all_y[valid_mask]
    all_yerr = all_yerr[valid_mask]
    
    # Compute weights
    weights = all_yerr / (all_y * np.log(10))
    
    # Replace zeros or negatives in weights
    min_weight = 1e-10
    weights[weights <= 0] = min_weight
    
    # Compute model predictions
    L_data = 10 ** all_x
    model_y = schechter(L_data, phi_best, Lstar_best, alpha_best)
    
    # Chi-squared calculation
    chi_squared = np.sum(((np.log10(all_y) - np.log10(model_y)) ** 2) / weights)
    
    # Degrees of freedom (3 parameters: phi, Lstar, alpha)
    dof = len(all_y) - 3
    
    # Reduced chi-squared
    reduced_chi2 = chi_squared / dof if dof > 0 else np.nan
    
    return {
        'chi_squared': chi_squared,
        'dof': dof,
        'reduced_chi2': reduced_chi2
    }


def get_confidence_intervals(samples, L_fit, percentiles=(2.5, 97.5)):
    """
    Calculate confidence intervals from MCMC samples.
    
    Parameters
    ----------
    samples : object
        MCMC samples (from mi.flatchain)
    L_fit : array-like
        Luminosity values for plotting
    percentiles : tuple, optional
        Lower and upper percentiles
        
    Returns
    -------
    dict
        Dictionary with 'lower_bound' and 'upper_bound' arrays
    """
    phi_samples = samples['phi']
    Lstar_samples = samples['Lstar']
    a_samples = samples['a']
    
    schechter_samples = np.array([
        schechter(L_fit, phi, Lstar, a)
        for phi, Lstar, a in zip(phi_samples, Lstar_samples, a_samples)
    ])
    
    lower_bound = np.percentile(schechter_samples, percentiles[0], axis=0)
    upper_bound = np.percentile(schechter_samples, percentiles[1], axis=0)
    
    return {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }
