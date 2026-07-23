import numpy as np
import pandas as pd
from scipy.stats import linregress

def generate_performance_metrics(df):
    returns = df['Strategy_Returns'].dropna()
    active_returns = returns[returns != 0]
    win_rate = (len(active_returns[active_returns > 0]) / len(active_returns)) * 100 if not active_returns.empty else 0.0
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std()) if returns.std() != 0 else 0.0
    cum_returns = (1 + returns).cumprod()
    max_drawdown = ((cum_returns - cum_returns.cummax()) / cum_returns.cummax()).min() * 100
    return win_rate, sharpe_ratio, max_drawdown

def calc_returns(prices):
    return prices.pct_change().dropna()

def get_beta(asset_ret, bench_ret):
    df = pd.concat([asset_ret, bench_ret], axis=1).dropna()
    df.columns = ['asset', 'benchmark']
    slope, intercept, r_value, p_value, std_err = linregress(df['benchmark'], df['asset'])
    return slope

def get_hedge_ratio(beta, target=0.0):
    return beta - target
