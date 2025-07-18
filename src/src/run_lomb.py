Lomb–Scargle power spectrum for unevenly spaced data (or evenly spaced with gaps).
Includes Monte Carlo significance (uniform random earthquake occurrence null model).
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from utils_io import load_main_excel, save_csv
from utils_filters import dropna_align

def lomb_astropy(t, y, dy=None, freq=None):
    from astropy.timeseries import LombScargle
    ls = LombScargle(t, y, dy=dy, nterms=1, normalization='psd')
    if freq is None:
        # auto frequency grid
        freq, power = ls.autopower()
    else:
        power = ls.power(freq)
    return freq, power

def lomb_scipy(t, y, freq):
    from scipy.signal import lombscargle
    # scipy expects angular frequency; also mean-subtract
    y = y - np.mean(y)
    p = lombscargle(t, y, freq)
    return freq, p

def monte_null_uniform(n_years, n_quakes, t, freq, n_mc=5000, rng=None):
    """
    Null: uniformly distributed events over years; convert to annual counts; compute LS power.
    Returns array (n_mc, n_freq).
    """
    if rng is None:
        rng = np.random.default_rng()
    mc_power = np.empty((n_mc, len(freq)))
    years = np.arange(n_years)
    for i in range(n_mc):
        # sample n_quakes years with replacement -> counts
        sim_counts = np.bincount(rng.integers(0, n_years, size=n_quakes), minlength=n_years)
        # align
        sim_counts = sim_counts.astype(float)
        # mean-subtract
        sim_counts -= sim_counts.mean()
        # compute LS
        from astropy
