import numpy as np
import pandas as pd
from signal_generator import generate_signals
from risk_management import (
    generate_performance_metrics, 
    calc_returns, 
    get_beta, 
    get_hedge_ratio
)

def run_vectorized_backtest(df, stop_loss_pct=0.08):
    df['Position'] = df['Signal'].replace(0, np.nan).ffill().fillna(0)
    df['Position'] = np.where(df['Position'] == -1, 0, df['Position'])
    
    df['Entry_Price'] = np.where((df['Position'] == 1) & (df['Position'].shift(1) == 0), df['Close'], np.nan)
    df['Entry_Price'] = df['Entry_Price'].ffill()
    df['Entry_Price'] = np.where(df['Position'] == 0, np.nan, df['Entry_Price'])
    
    df['Trade_Drawdown'] = (df['Close'] - df['Entry_Price']) / df['Entry_Price']
    
    stop_loss_cond = df['Trade_Drawdown'] <= -stop_loss_pct
    df.loc[stop_loss_cond, 'Signal'] = -1 
    
    df['Position'] = df['Signal'].replace(0, np.nan).ffill().fillna(0)
    df['Position'] = np.where(df['Position'] == -1, 0, df['Position'])
    
    df['Position'] = df['Position'].shift(1).fillna(0)
    df['Market_Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Market_Returns']
    return df

def calculate_kelly_criterion(strategy_returns, fraction=0.25):
    active_returns = strategy_returns[strategy_returns != 0].dropna()
    if active_returns.empty: return 0.0, 0.0
    
    win_rate = len(active_returns[active_returns > 0]) / len(active_returns)
    avg_win = active_returns[active_returns > 0].mean() if not active_returns[active_returns > 0].empty else 0
    avg_loss = abs(active_returns[active_returns < 0].mean()) if not active_returns[active_returns < 0].empty else 1e-9
    win_loss_ratio = avg_win / avg_loss
    
    if win_loss_ratio == 0: return 0.0, 0.0
    
    full_kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
    full_kelly = max(0.0, min(full_kelly, 1.0))
    fractional_kelly = full_kelly * fraction
    return full_kelly, fractional_kelly

def main():
    asset_file = 'asset_data.csv'
    bench_file = 'benchmark_data.csv'
    
    try:
        df = pd.read_csv(asset_file, index_col=0, parse_dates=True)
        bench_df = pd.read_csv(bench_file, index_col=0, parse_dates=True)
        
        df.rename(columns={'close': 'Close', 'volume': 'Volume'}, inplace=True)
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        df = df.dropna(subset=['Close', 'Volume'])
        
        bench_prices = bench_df['Close'] if 'Close' in bench_df.columns else bench_df.iloc[:, 0]
    except FileNotFoundError:
        print("Error: Could not find asset_data.csv or benchmark_data.csv.")
        return

    df = generate_signals(df)
    df = run_vectorized_backtest(df, stop_loss_pct=0.08)
    
    win_rate, sharpe, mdd = generate_performance_metrics(df)
    full_k, safe_k = calculate_kelly_criterion(df['Strategy_Returns'], fraction=0.25)
    
    asset_ret = calc_returns(df['Close'])
    bench_ret = calc_returns(bench_prices)
    beta = get_beta(asset_ret, bench_ret)
    hr = get_hedge_ratio(beta)
    
    clean_asset = df['Close'].dropna()
    clean_bench = bench_prices.dropna()
    
    total_asset_return = (clean_asset.iloc[-1] / clean_asset.iloc[0] - 1) * 100
    total_bench_return = (clean_bench.iloc[-1] / clean_bench.iloc[0] - 1) * 100
    
    strategy_cum = (1 + df['Strategy_Returns'].dropna()).cumprod()
    total_strategy_return = (strategy_cum.iloc[-1] - 1) * 100 if not strategy_cum.empty else 0.0
    
    print("\n--- Week 5 Combined Strategy Performance ---")
    print(f"Total Trading Days Assessed: {len(df)}")
    print(f"Win Rate:                    {win_rate:.2f}%")
    print(f"Annualized Sharpe Ratio:     {sharpe:.4f}")
    print(f"Maximum Drawdown:            {mdd:.2f}%")
    print("-" * 44)
    print(f"Total Strategy Return:       {total_strategy_return:.2f}%")
    print(f"Total Asset Return:          {total_asset_return:.2f}% (Buy & Hold)")
    print(f"Total Benchmark Return:      {total_bench_return:.2f}% (Buy & Hold)")
    print("-" * 44)
    print(f"Theoretical Full Kelly:      {full_k * 100:.2f}% (High Risk)")
    print(f"Optimal Quarter-Kelly Bet:   {safe_k * 100:.2f}% of capital")
    print("-" * 44)
    print(f"Asset Beta vs Benchmark:     {beta:.4f}")
    print(f"Required Hedge Ratio:        {hr:.4f}")

    port_val = 100000
    if hr > 0:
        print(f"Action: For a ${port_val} long position, short ${port_val * hr:.2f} of the benchmark.")
    else:
        print(f"Action: For a ${port_val} long position, go long ${abs(port_val * hr):.2f} of the benchmark.")

if __name__ == "__main__":
    main()
