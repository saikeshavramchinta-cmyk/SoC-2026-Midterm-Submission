import pandas as pd
from indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands, calculate_sma
from filters import apply_volume_filter

def generate_signals(df):
    df = calculate_macd(df)
    df = calculate_rsi(df, period=14)
    df = calculate_bollinger_bands(df, period=20, num_std=2) 
    df = apply_volume_filter(df, period=20)
    
    # Calculate macro, micro, and fast trailing trends
    df = calculate_sma(df, period=200) 
    df = calculate_sma(df, period=50)  
    df = calculate_sma(df, period=20)  # Fast trailing stop baseline
    
    df['Signal'] = 0
    
    # BUY LOGIC: High Market Exposure
    buy_cond = (
        (df['Close'] > df['SMA_200']) &                  
        (df['MACD_Line'] > df['Signal_Line']) &          
        (df['Volume_Filter_Pass'] == True)
    )
    
    # SELL LOGIC: Let Winners Run!
    sell_cond = (
        (df['Close'] < df['SMA_20']) |                   # Fast trend breaks
        (df['MACD_Line'] < df['Signal_Line'])            # Momentum flips bearish
    )
    
    df.loc[buy_cond, 'Signal'] = 1
    df.loc[sell_cond, 'Signal'] = -1
    return df
