import pandas as pd

def apply_volume_filter(df, period=20):
    df['Volume_SMA_20'] = df['Volume'].rolling(window=period).mean()
    df['Volume_Filter_Pass'] = df['Volume'] > df['Volume_SMA_20']
    return df
