
import pandas as pd
from pathlib import Path

def load_main_excel(path, year_min=1600, year_max=1900):
    """
    Expected columns (case-insensitive contains):
      year
      earthquake  (EQ 50–60 yr component OR raw; we keep original name & let user map)
      Number of Earthquakes
      Solar Radiative 1
      Solar Radiative 2
      Solar Radiative 3   (optional)
    """
    df = pd.read_excel(path)
    # normalize column names
    colmap = {}
    for c in df.columns:
        cl = str(c).strip().lower()
        if 'year' in cl:
            colmap[c] = 'Year'
        elif cl.startswith('earthquake'):
            colmap[c] = 'EQ_comp'   # your 50–60 yr coeff
        elif 'number' in cl and 'earthquake' in cl:
            colmap[c] = 'EQ_count'
        elif 'radiative 1' in cl:
            colmap[c] = 'Solar1'
        elif 'radiative 2' in cl:
            colmap[c] = 'Solar2'
        elif 'radiative 3' in cl:
            colmap[c] = 'Solar3'
        else:
            # pass-through
            colmap[c] = c
    df = df.rename(columns=colmap)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df[df['Year'].between(year_min, year_max)].sort_values('Year').reset_index(drop=True)
    return df

def save_csv(df, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[saved] {path}")
