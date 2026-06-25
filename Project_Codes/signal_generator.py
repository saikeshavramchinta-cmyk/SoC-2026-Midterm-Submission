import pandas as pd
from scipy.io import loadmat

# Import our custom indicators
from indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands
from filters import apply_volume_filter

def generate_signals(df):
    # Apply all indicators to the dataframe
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger_bands(df)
    df = apply_volume_filter(df)
    
    # Default everything to hold
    df['Signal'] = 0
    
    # Buy logic: price near/below lower band, oversold RSI, high volume, and MACD crossing up
    buy_cond = (
        (df['Close'] <= df['BB_Lower']) & 
        (df['RSI'] < 40) & 
        (df['Volume_Filter_Pass']) &  # no need for == True
        (df['MACD_Line'] > df['Signal_Line']) & 
        (df['MACD_Line'].shift(1) <= df['Signal_Line'].shift(1))
    )
    
    # Sell logic: price hits upper band OR MACD crosses down (momentum dying)
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
    filename = "market_data.mat" 
    
    try:
        # Load the .mat file
        mat = loadmat(filename)
        
        # Extract and flatten the matrices into standard 1D pandas columns
        df = pd.DataFrame({
            'Close': mat['Close'].flatten(),
            'Volume': mat['Volume'].flatten()
        })
        
        # Grab the target/original signals if they are included in the file
        if 'Original_Signal' in mat:
            df['Original_Signal'] = mat['Original_Signal'].flatten()
            
    except FileNotFoundError:
        print(f"Error: Could not find {filename}. Make sure it's in the same directory.")
        return
    except KeyError as e:
        print(f"Error: Missing expected variable in the .mat file - {e}")
        return
    
    # Run the engine
    final_df = generate_signals(df)
    get_performance(final_df)
    
    # Compare against original signals if we have them
    if 'Original_Signal' in final_df.columns:
        matches = (final_df['Signal'] == final_df['Original_Signal']).sum()
        total = len(final_df)
        print(f"Matches against original: {matches}/{total} ({(matches/total)*100:.2f}%)")

if __name__ == "__main__":
    main()
