import pandas as pd
def calculate_macd(df):
    # Calculates the standard MACD and Signal lines.
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Line'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()
    return df

def calculate_rsi(df, period=14):
    # Calculates the standard 14-period RSI.
    df['Price_Change'] = df['Close'].diff()
    df['Gain'] = df['Price_Change'].where(df['Price_Change'] > 0, 0)
    df['Loss'] = -df['Price_Change'].where(df['Price_Change'] < 0, 0)
    
    df['Avg_Gain'] = df['Gain'].rolling(window=period).mean()
    df['Avg_Loss'] = df['Loss'].rolling(window=period).mean()
    
    df['RS'] = df['Avg_Gain'] / df['Avg_Loss']
    df['RSI'] = 100 - (100 / (1 + df['RS']))
    return df

def calculate_bollinger_bands(df, period=20, num_std=2):
    # Calculates the Middle, Upper, and Lower Bollinger Bands.
    df['BB_Middle'] = df['Close'].rolling(window=period).mean()
    rolling_std = df['Close'].rolling(window=period).std()
    
    df['BB_Upper'] = df['BB_Middle'] + (num_std * rolling_std)
    df['BB_Lower'] = df['BB_Middle'] - (num_std * rolling_std)
    return df
    
