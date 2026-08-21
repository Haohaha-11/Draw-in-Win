import pandas as pd
import numpy as np

files = ['Laissez_faire.csv', 'Aggressive.csv', 'Bankrupt.csv', 'Ours.csv']

for f in files:
    df = pd.read_csv(f)
    print(f'\n{f}:')
    print(f'  I range: {df["I"].min():.6f} - {df["I"].max():.6f}')
    print(f'  I mean: {df["I"].mean():.6f}, std: {df["I"].std():.6f}')
    print(f'  Pop range: {df["Pop"].min():.6f} - {df["Pop"].max():.6f}')
    print(f'  Data points: {len(df)}')
