import pandas as pd
from scipy.io import loadmat  # Required to read MATLAB .mat files

# Import packages from our other local files
from indicators import calculate_macd, calculate_rsi, calculate_bollinger_bands
from filters import apply_volume_filter

def generate_signals(df):
    """
    Generates trading signals using Bollinger Bands, MACD, RSI, and Volume Filters.
    """
    # 1. Run all indicator math and filter sets on our dataframe
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger_bands(df)
    df = apply_volume_filter(df)
    
    # 2. Set default position column to Hold (0)
    df['Signal'] = 0
    
    # 3. Formulate Confluence Strategy Rules
    
    # BUY: Price is low (<= BB_Lower) AND RSI < 40 AND high volume AND MACD upward crossover
    buy_condition = (
        (df['Close'] <= df['BB_Lower']) & 
        (df['RSI'] < 40) & 
        (df['Volume_Filter_Pass'] == True) &
        (df['MACD_Line'] > df['Signal_Line']) & 
        (df['MACD_Line'].shift(1) <= df['Signal_Line'].shift(1))
    )
    
    # SELL: Price touches overextended band (>= BB_Upper) OR MACD breaks downward
    sell_condition = (
        (df['Close'] >= df['BB_Upper']) | 
        ((df['MACD_Line'] < df['Signal_Line']) & (df['MACD_Line'].shift(1) >= df['Signal_Line'].shift(1)))
    )
    
    # 4. Map the buy and sell conditions into our Signal tracker
    df.loc[buy_condition, 'Signal'] = 1
    df.loc[sell_condition, 'Signal'] = -1
    
    return df

def calculate_performance(df):
    """Calculates basic win rate metrics on the strategy signals."""
    df['Next_Day_Price_Change'] = df['Close'].shift(-1) - df['Close']
    trades = df[df['Signal'] != 0].copy()
    
    if trades.empty:
        print("No strategy entry or exit triggers identified in this dataset.")
        return
        
    trades['Is_Win'] = (trades['Signal'] * trades['Next_Day_Price_Change']) > 0
    
    total_trades = len(trades)
    winning_trades = trades['Is_Win'].sum()
    win_rate = (winning_trades / total_trades) * 100
    
    print("\n=== CONFLUENCE STRATEGY PERFORMANCE ===")
    print(f"Total Trades Taken: {total_trades}")
    print(f"Winning Trades: {winning_trades}")
    print(f"Strategy Win Rate: {win_rate:.2f}%\n")

def main():
    # Here we should add our own .mat type dataset by removing the market_data.mat
    file_path = "market_data.mat" 
    
    try:
        print(f"Opening and parsing MATLAB data from: {file_path}")
        
        # 1. Load the .mat file into a Python dictionary
        mat_data = loadmat(file_path)
        
        # 2. Extract the arrays and build our DataFrame
        try:
            # MATLAB variables import as 2D arrays (matrices). 
            # .flatten() converts them into standard 1D lists for pandas.
            close_prices = mat_data['Close'].flatten()
            volumes = mat_data['Volume'].flatten()
            
            data_from_file = pd.DataFrame({
                'Close': close_prices,
                'Volume': volumes
            })
            
            # If the .mat file also contains the original signals for grading, pull them in too
            if 'Original_Signal' in mat_data:
                data_from_file['Original_Signal'] = mat_data['Original_Signal'].flatten()
                
        except KeyError as e:
            print(f"\n[Data Error] The .mat file is missing a required variable: {e}")
            print("Please ensure your MATLAB workspace saved variables specifically named 'Close' and 'Volume'.")
            return
        
        # 3. Run our automated signal compilation engine
        final_df = generate_signals(data_from_file)
        calculate_performance(final_df)
        
        # 4. Check against grading keys or target metrics if they exist in file
        original_column_name = 'Original_Signal' 
        if original_column_name in final_df.columns:
            matching_rows = (final_df['Signal'] == final_df[original_column_name]).sum()
            total_rows = len(final_df)
            match_accuracy = (matching_rows / total_rows) * 100
            
            print("=== ACCURACY AGAINST ORIGINAL ===")
            print(f"Matches found: {matching_rows} out of {total_rows} records")
            print(f"Match Accuracy: {match_accuracy:.2f}%")
            
    except FileNotFoundError:
        print(f"\n[Execution Error] Local target file '{file_path}' could not be located.")

if __name__ == "__main__":
    main()
