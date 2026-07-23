import pandas as pd
from scipy.io import loadmat

# Import our custom indicators
from indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands, calculate_sma
from filters import apply_volume_filter

def generate_signals(df):
    # Apply all indicators to the dataframe
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger_bands(df)
    df = apply_volume_filter(df)
    df = calculate_sma(df, 200)
    
    # Default everything to hold
    df['Signal'] = 0
    
    # Buy logic: price near/below lower band, oversold RSI, high volume, and MACD crossing up
    buy_cond = (
        (df['Close'] <= df['BB_Lower']) & 
        (df['RSI'] < 30) &               # Stricter oversold threshold
        (df['Close'] > df['SMA_200']) &  # Regime Filter: Only buy in uptrends
        (df['MACD_Line'] > df['Signal_Line']) & 
        (df['MACD_Line'].shift(1) <= df['Signal_Line'].shift(1))
    )
    
    sell_cond = (
        (df['Close'] >= df['BB_Upper']) | 
        ((df['MACD_Line'] < df['Signal_Line']) & (df['MACD_Line'].shift(1) >= df['Signal_Line'].shift(1)))
    )
    
    df.loc[buy_cond, 'Signal'] = 1
    df.loc[sell_cond, 'Signal'] = -1
    
    return df

def get_performance(df):
    # Calculate next day's price change to see if our trade was right
    df['next_day_change'] = df['Close'].shift(-1) - df['Close']
    trades = df[df['Signal'] != 0].copy()
    
    if trades.empty:
        print("No trades triggered.")
        return
        
    # It's a win if the signal direction matches the price movement direction
    trades['is_win'] = (trades['Signal'] * trades['next_day_change']) > 0
    
    total = len(trades)
    wins = trades['is_win'].sum()
    win_rate = (wins / total) * 100
    
    print(f"Total trades: {total}")
    print(f"Wins: {wins}")
    print(f"Win Rate: {win_rate:.2f}%")

def main():
    # Change this to whatever your dataset is named
    filename = "market_data.csv" 
    
    try:
        # Load the CSV
        df = pd.read_csv(filename)
        
        # Standardize column names
        df.rename(columns={'close': 'Close', 'volume': 'Volume'}, inplace=True)
        
        # Force numeric types to prevent the pandas DataError
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        
        # Drop the rows containing text headers that were converted to NaN
        df = df.dropna(subset=['Close', 'Volume'])
            
    except FileNotFoundError:
        print(f"Error: Could not find {filename}. Make sure get_data.py ran successfully.")
        return
    
    # Run the engine
    final_df = generate_signals(df)
    get_performance(final_df)

if __name__ == "__main__":
    main()
