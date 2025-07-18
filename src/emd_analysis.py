
# -*- coding: utf-8 -*-
"""
Perform EMD on a selected series (e.g., annual earthquake counts) and save IMFs.
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from utils_io import load_main_excel, save_csv

def do_emd(y):
    try:
        from PyEMD import EMD
    except ImportError as e:
        raise SystemExit("PyEMD not installed. pip install PyEMD") from e
    emd = EMD()
    imfs = emd.emd(y)   # shape (n_imf, n_points)
    return imfs

def main(args):
    df = load_main_excel(args.input, args.year_min, args.year_max)
    if args.series == 'EQ_count':
        y = df['EQ_count'].values.astype(float)
    elif args.series == 'EQ_comp':
        y = df['EQ_comp'].values.astype(float)
    else:
        y = df[args.series].values.astype(float)

    imfs = do_emd(y)
    # Build dataframe
    out = pd.DataFrame({'Year': df['Year']})
    for i in range(imfs.shape[0]):
        out[f'IMF{i+1}'] = imfs[i]
    out['Residual'] = y - imfs.sum(axis=0)

    save_csv(out, args.output)

    if args.print_energy:
        tot = np.sum(y**2)
        print("IMF energy fractions:")
        for i in range(imfs.shape[0]):
            frac = np.sum(imfs[i]**2) / tot
            print(f"  IMF{i+1}: {frac:0.3f}")
        print(f"Residual energy: {(np.sum(out['Residual']**2)/tot):0.3f}")


