"""
Data loading and preprocessing utilities.

This module handles loading H-alpha databases from CSV and Excel files,
and preparing data for fitting.
"""

import pandas as pd
import numpy as np


def load_ha_database(csv_path):
    """
    Load H-alpha database from CSV file.
    
    Parameters
    ----------
    csv_path : str
        Path to CSV file
        
    Returns
    -------
    pandas.DataFrame
        Processed database
    """
    # Load CSV
    Ha_Database = pd.read_csv(csv_path)
    Ha_Database = Ha_Database.iloc[:-6]
    Ha_Database = Ha_Database.drop(index=0)
    
    # Make sure all values are numeric
    cols_to_convert = [
        "z", "z_low", "z_upp", 
        "log(L_Ha)", "log(L_Ha)_upper", "log(L_Ha)_low",
        "phi_Ha", "phi_Ha_upp", "phi_Ha_low",
        "a_Ha", "a_Ha_upp", "a_Ha_low",
        "SFRD", "SFRD_upp", "SFRD_low"
    ]
    Ha_Database[cols_to_convert] = Ha_Database[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    
    return Ha_Database


def load_excel_sheets(excel_path, sheets_to_load=None):
    """
    Load multiple sheets from Excel file into a dictionary.
    
    Parameters
    ----------
    excel_path : str
        Path to Excel file
    sheets_to_load : list, optional
        List of sheet names to load. If None, loads default sheets.
        
    Returns
    -------
    dict
        Dictionary mapping sheet names to DataFrames
    """
    if sheets_to_load is None:
        sheets_to_load = [
            'Ha_Database_20250210', 'Schechter_Params', 'CSFD',
            'Gallego 1995', 'Tresse 1998', 'Yan 1999', 'Sullivan 2000', 'Moorwood 2000',
            'Hopkins 2000', 'Sun 2023', 'Tresse 2002', 'Fujita 2003', 'Hippelein 2003',
            'Pascual 2005', 'Shioya 2008', 'Drake 2013', 'Covelo-Paz 2024', 'Hayes 2010',
            'Morioka 2008', 'Villar 2008', 'Stroe 2015', 'Sobral 2013', 'Bollo 2023',
            'Colbert 2013', 'Gomez 2016', 'Lee 2012', 'Guo 2024', 'Ly 2007'
        ]
    
    xls = pd.ExcelFile(excel_path)
    data = {sheet: pd.read_excel(xls, sheet) for sheet in sheets_to_load}
    
    return data


def prepare_redshift_bins(df, z_bins=None):
    """
    Prepare data organized by redshift bins.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with plotted data including 'redshift_bin' column
    z_bins : list of tuples, optional
        List of (z_min, z_max) tuples. If None, uses default bins.
        
    Returns
    -------
    dict
        Dictionary mapping redshift bin labels to filtered DataFrames
    """
    if z_bins is None:
        z_bins = [(0, 0.25), (0.26, 0.5), (0.51, 0.83), (0.84, 2), (2.1, 4), (4.01, 7)]
    
    bin_data = {}
    unique_bins = df['redshift_bin'].unique()
    
    for i, (z_min, z_max) in enumerate(z_bins):
        if i < len(unique_bins):
            bin_label = unique_bins[i]
            bin_data[bin_label] = df[df['redshift_bin'] == bin_label]
    
    return bin_data


def extract_data_for_fitting(df_bin):
    """
    Extract x, y, and yerr arrays from a binned DataFrame for fitting.
    
    Parameters
    ----------
    df_bin : pandas.DataFrame
        DataFrame for a specific redshift bin
        
    Returns
    -------
    tuple
        (all_x, all_y, all_yerr) as numpy arrays
    """
    all_x = []
    all_y = []
    all_yerr = []
    
    datasets = df_bin['dataset'].unique()
    
    for dataset in datasets:
        subset = df_bin[df_bin['dataset'] == dataset]
        
        x = subset['log_L_Ha_W'].values
        y = subset['phi_L'].values
        yerr_low = subset['phi_err_low'].values
        yerr_up = subset['phi_err_up'].values
        
        # Compute average yerr for fitting
        avgyerr = (yerr_low + yerr_up) / 2
        
        # Store values for fit
        all_x.extend(x)
        all_y.extend(y)
        all_yerr.extend(avgyerr.tolist())
    
    return np.array(all_x), np.array(all_y), np.array(all_yerr)


def export_plotted_data(plotted_data, output_path='plotted_data.csv'):
    """
    Export plotted data dictionary to CSV.
    
    Parameters
    ----------
    plotted_data : dict
        Dictionary with redshift bins and datasets
    output_path : str, optional
        Output CSV file path
        
    Returns
    -------
    pandas.DataFrame
        The exported DataFrame
    """
    rows = []
    for z_bin, datasets in plotted_data.items():
        for sheet_name, values in datasets.items():
            for x_val, y_val, yerr_low, yerr_up in zip(
                values['x'], values['y'],
                values['yerr'][0], values['yerr'][1]
            ):
                rows.append({
                    'redshift_bin': z_bin,
                    'dataset': sheet_name,
                    'log_L_Ha_W': x_val,
                    'phi_L': y_val,
                    'phi_err_low': yerr_low,
                    'phi_err_up': yerr_up
                })
    
    df_export = pd.DataFrame(rows)
    df_export.to_csv(output_path, index=False)
    
    return df_export
