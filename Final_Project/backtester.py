import pandas as pd
from signal_generator import generate_signals
from risk_management import (
    run_vectorized_backtest, 
    generate_performance_metrics, 
    calculate_kelly_criterion, 
    calc_returns, 
    get_beta, 
    get_hedge_ratio
)

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
