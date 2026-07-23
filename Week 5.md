## The Kelly Criterion (Optimal Sizing)
The Kelly Criterion is a mathematical formula that finds the exact bet size required to maximize the long-term compound growth rate of your capital.For a discrete scenario (like a coin toss or a simple trade with a fixed stop-loss and take-profit), the formula is:
## $$f^* = \frac{bp - q}{b}$$
Where:

### $f^*$ = The optimal fraction of your bankroll to allocate.
### $p$ = The probability of a win (e.g., $0.55$ for $55\%$).
### $q$ = The probability of a loss ($1 - p$).
### $b$ = The odds received, or the ratio of the average win to the average loss. (If you risk $\$100$ to make $\$150$, $b = 1.5$).
## The Continuous (Finance) Variation
In quantitative finance, asset prices don't behave like simple coin flips. When returns are modeled as continuous variables, the formula (often called Merton's fraction) adapts to use expected returns and volatility:
## $$f^* = \frac{\mu - r}{\sigma^2}$$
Where 
$\mu$ is the expected return, $r$ is the risk-free rate, and $\sigma^2$ is the variance (volatility squared).

Performance Metrics
Once you apply a sizing model, you need to measure how the strategy actually behaves.
## Sharpe Ratio
The Sharpe Ratio measures the "efficiency" of your returns. It tells you how much excess return you are generating for every unit of volatility you endure.
$$S = \frac{R_p - R_f}{\sigma_p}$$
$R_p$ = The return of the portfolio/strategy.
$R_f$ = The risk-free rate (e.g., the yield on a government bond).
$\sigma_p$ = The standard deviation of the portfolio's returns (volatility).
What it means: A Sharpe ratio of $1.0$ is generally considered good, while $>2.0$ is excellent. If a strategy makes $20\%$ a year but wildly swings up and down $40\%$ a month, it has a low Sharpe ratio.
Maximum Drawdown (MDD)
If the Sharpe ratio is about efficiency, MDD is about pain tolerance. It measures the worst-case scenario: the largest single percentage drop from an all-time high in your equity curve to the subsequent lowest point.$$\text{MDD} = \frac{\text{Peak Value} - \text{Trough Value}}{\text{Peak Value}}$$
What it means: If your account grows from $\$100 \rightarrow \$200$, drops to $\$100$, and then grows to $\$300$, your Maximum Drawdown is $50\%$ (the drop from $200$ to $100$). Many hedge funds strictly monitor MDD because a $50\%$ drawdown requires a $100\%$ return just to get back to breakeven.
## Win Rate
Win rate is simply your accuracy.$$\text{Win Rate} = \frac{\text{Number of Winning Trades}}{\text{Total Number of Trades}}
$$What it means:
Win rate is highly contextual. A trend-following strategy might only have a $35\%$ win rate but still be highly profitable if its winners are 4x the size of its losers (high $b$ in the Kelly formula). Conversely, a strategy with a $95\%$ win rate will eventually blow up the account if the $5\%$ of losses are catastrophic.
