import numpy as np
import pandas as pd

# ==========================================
# 1. INDICATORS & FILTERS
# ==========================================
def calculate_macd(df):
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Line'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()
    return df

def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def calculate_bollinger_bands(df, period=20, num_std=2):
    df['BB_Middle'] = df['Close'].rolling(window=period).mean()
    rolling_std = df['Close'].rolling(window=period).std()
    df['BB_Upper'] = df['BB_Middle'] + (num_std * rolling_std)
    df['BB_Lower'] = df['BB_Middle'] - (num_std * rolling_std)
    return df

def apply_volume_filter(df, period=20):
    df['Volume_SMA_20'] = df['Volume'].rolling(window=period).mean()
    df['Volume_Filter_Pass'] = df['Volume'] > df['Volume_SMA_20']
    return df

def calculate_sma(df, period):
    df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
    return df
# ==========================================
# 2. SIGNAL GENERATION (Volatility-Based Exits)
# ==========================================
def generate_signals(df):
    df = calculate_macd(df)
    df = calculate_rsi(df, period=14)
    # Ensure Bollinger Bands are using 2 standard deviations
    df = calculate_bollinger_bands(df, period=20, num_std=2) 
    df = apply_volume_filter(df, period=20)
    
    # Calculate macro and micro trends
    df = calculate_sma(df, period=200) 
    df = calculate_sma(df, period=50)  
    
    df['Signal'] = 0
    
    # BUY LOGIC: Macro/Micro Uptrend, Momentum shifting up, not overbought
    buy_cond = (
        (df['Close'] > df['SMA_200']) &                  
        (df['Close'] > df['SMA_50']) &                   
        (df['RSI'] < 65) &                               
        (df['Volume_Filter_Pass'] == True) &             
        (df['MACD_Line'] > df['Signal_Line']) &          
        (df['MACD_Line'].shift(1) <= df['Signal_Line'].shift(1)) 
    )
    
    # SELL LOGIC: Volatility-Based Take Profit & Trend Break
    # 1. Take profit immediately when price hits the Upper Bollinger Band (+2 Std Dev).
    # 2. Exit if the 50-day trend breaks to protect capital if the setup fails to launch.
    sell_cond = (
        (df['Close'] >= df['BB_Upper']) |                
        (df['Close'] < df['SMA_50'])                               
    )
    
    df.loc[buy_cond, 'Signal'] = 1
    df.loc[sell_cond, 'Signal'] = -1
    return df

# ==========================================
# 3. BACKTESTER ENGINE (Long-Only + Stop-Loss)
# ==========================================
def run_vectorized_backtest(df, stop_loss_pct=0.08):
    # 1. Convert triggers to a continuous holding position
    df['Position'] = df['Signal'].replace(0, np.nan).ffill().fillna(0)
    
    # THE FIX: Force the strategy to be Long-Only (Convert -1 short positions to 0 flat positions)
    df['Position'] = np.where(df['Position'] == -1, 0, df['Position'])
    
    # 2. Track Entry Price for active trades
    df['Entry_Price'] = np.where((df['Position'] == 1) & (df['Position'].shift(1) == 0), df['Close'], np.nan)
    df['Entry_Price'] = df['Entry_Price'].ffill()
    df['Entry_Price'] = np.where(df['Position'] == 0, np.nan, df['Entry_Price'])
    
    # 3. Calculate trade drawdown and trigger stop loss
    df['Trade_Drawdown'] = (df['Close'] - df['Entry_Price']) / df['Entry_Price']
    
    # If drawdown exceeds our threshold, force a sell signal (-1)
    stop_loss_cond = df['Trade_Drawdown'] <= -stop_loss_pct
    df.loc[stop_loss_cond, 'Signal'] = -1 
    
    # Recalculate Position after stop-loss exits
    df['Position'] = df['Signal'].replace(0, np.nan).ffill().fillna(0)
    # THE FIX: Re-apply the Long-Only constraint after stop-losses are injected
    df['Position'] = np.where(df['Position'] == -1, 0, df['Position'])
    
    # 4. Shift position by 1 to prevent look-ahead bias
    df['Position'] = df['Position'].shift(1).fillna(0)
    
    # 5. Calculate market returns and strategy returns
    df['Market_Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Market_Returns']
    return df

def calculate_kelly_criterion(strategy_returns, fraction = 0.25):
    """
    Calculates the Kelly Criterion and applies a fractional multiplier 
    to account for parameter uncertainty and minimize variance drag.
    Default is Quarter-Kelly (0.25).
    """
    active_returns = strategy_returns[strategy_returns != 0].dropna()
    if active_returns.empty: return 0.0, 0.0
    
    win_rate = len(active_returns[active_returns > 0]) / len(active_returns)
    avg_win = active_returns[active_returns > 0].mean() if not active_returns[active_returns > 0].empty else 0
    avg_loss = abs(active_returns[active_returns < 0].mean()) if not active_returns[active_returns < 0].empty else 1e-9
    win_loss_ratio = avg_win / avg_loss
    
    if win_loss_ratio == 0: return 0.0, 0.0
    
    # Calculate Full Kelly
    full_kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
    full_kelly = max(0.0, min(full_kelly, 1.0))
    
    # Calculate Fractional Kelly
    fractional_kelly = full_kelly * fraction
    
    return full_kelly, fractional_kelly

def generate_performance_metrics(df):
    returns = df['Strategy_Returns'].dropna()
    active_returns = returns[returns != 0]
    win_rate = (len(active_returns[active_returns > 0]) / len(active_returns)) * 100 if not active_returns.empty else 0.0
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std()) if returns.std() != 0 else 0.0
    cum_returns = (1 + returns).cumprod()
    max_drawdown = ((cum_returns - cum_returns.cummax()) / cum_returns.cummax()).min() * 100
    return win_rate, sharpe_ratio, max_drawdown
# ==========================================
# 4. EXECUTION
# ==========================================
def main():
    filename = "market_data.csv"
    try:
        df = pd.read_csv(filename)
        df.rename(columns={'close': 'Close', 'volume': 'Volume'}, inplace=True)
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        df = df.dropna(subset=['Close', 'Volume'])
    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
        return

    df = generate_signals(df)
    df = run_vectorized_backtest(df, stop_loss_pct=0.08)
    
    win_rate, sharpe, mdd = generate_performance_metrics(df)
    
    # Unpack both the dangerous theoretical max and the safe applied fraction
    full_k, safe_k = calculate_kelly_criterion(df['Strategy_Returns'], fraction=0.25)
    
    print("\n--- Final V3 Strategy Performance ---")
    print(f"Total Trading Days Assessed: {len(df)}")
    print(f"Win Rate:                    {win_rate:.2f}%")
    print(f"Annualized Sharpe Ratio:     {sharpe:.4f}")
    print(f"Maximum Drawdown:            {mdd:.2f}%")
    print("-" * 44)
    print(f"Theoretical Full Kelly:      {full_k * 100:.2f}% (High Risk)")
    print(f"Optimal Quarter-Kelly Bet:   {safe_k * 100:.2f}% of capital")

if __name__ == "__main__":
    main()
