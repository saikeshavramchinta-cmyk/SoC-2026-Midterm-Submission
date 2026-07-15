import pandas as pd
import numpy as np
from scipy.stats import linregress

def calc_returns(prices):
    # Calculate daily percentage returns and drop the first NaN
    return prices.pct_change().dropna()

def get_beta(asset_ret, bench_ret):
    # Combine and drop NAs to make sure dates align perfectly
    df = pd.concat([asset_ret, bench_ret], axis=1).dropna()
    df.columns = ['asset', 'benchmark']
    
    # Run OLS regression to find the slope (Beta)
    slope, intercept, r_value, p_value, std_err = linregress(df['benchmark'], df['asset'])
    return slope

def get_hedge_ratio(beta, target=0.0):
    # Hedge ratio is just the difference between current and target beta
    return beta - target

if __name__ == "__main__":
    # File paths - update these to match your actual csv names
    asset_file = 'asset_data.csv'
    bench_file = 'benchmark_data.csv'
    
    # Read the datasets
    # Assumes the first column is the Date index
    asset_df = pd.read_csv(asset_file, index_col=0, parse_dates=True)
    bench_df = pd.read_csv(bench_file, index_col=0, parse_dates=True)
    
    # Extract the prices (change 'Close' if your data uses 'Adj Close' etc.)
    asset_prices = asset_df['Close']
    bench_prices = bench_df['Close']

    # 1. Calculate Returns
    asset_ret = calc_returns(asset_prices)
    bench_ret = calc_returns(bench_prices)

    # 2. Estimate Beta
    beta = get_beta(asset_ret, bench_ret)
    print(f"Asset Beta: {beta:.4f}")

    # 3. Compute Hedge Ratio
    hr = get_hedge_ratio(beta)
    print(f"Hedge Ratio: {hr:.4f}")

    # Quick example of what this means for a portfolio
    port_val = 100000
    print("\n--- Position Sizing ---")
    if hr > 0:
        print(f"For a ${port_val} long position, short ${port_val * hr:.2f} of the benchmark.")
    else:
        print(f"For a ${port_val} long position, go long ${abs(port_val * hr):.2f} of the benchmark.")
