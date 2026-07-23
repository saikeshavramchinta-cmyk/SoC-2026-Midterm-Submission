Part 1: The Five-File Architecture
1. indicators.py (The Measuring Tools)
This file is the math department. It takes raw price data and transforms it into useful statistics. Instead of cluttering our main logic with raw calculations, this file cleanly generates the Moving Averages, MACD, RSI, and Bollinger Bands. If you ever want to add a new indicator in the future, it goes here.

2. filters.py (The Bouncer)
This file decides what data is actually worth looking at. Currently, it holds our volume filter. It ensures we are only trading assets that have high liquidity, protecting the algorithm from getting stuck in low-volume stocks where a single large order could crash the price.

3. signal_generator.py (The Brain)
This is where the actual trading decisions are made. It imports the tools from indicators.py and filters.py, mixes them together, and asks the ultimate question: Should we buy, sell, or do nothing today? It outputs clear 1 (buy) and -1 (sell) signals based on our exact strategy rules.

4. risk_management.py (The Safety Net)
This file is dedicated strictly to evaluating performance and protecting capital. It doesn't care when we bought or sold; it only cares about the results. It calculates how much we made, how much risk we took (Sharpe Ratio), how bad the worst loss was (Maximum Drawdown), and how to hedge against a market crash using Beta.

5. backtester.py (The Time Machine)
This is the master execution script. It loads the historical market data, passes it through the signal generator, applies a strict 8% emergency stop-loss, and then runs the trade history through the risk management file. It stitches all the other files together to simulate exactly how this strategy would have performed in the past.

Part 2: Why We Chose These Specific Indicators
We built the engine to track a variety of indicators, but our final strategy relies heavily on a specific combination of them. Here is why:

200-Day and 50-Day SMAs (The Macro Trend): We use Simple Moving Averages because trading against the broader market trend is a losing game. The 200-day SMA tells us if the asset is in a long-term bull market. If the price is below this line, the algorithm completely ignores it. We only want to swim with the current, never against it.

MACD (The Momentum Trigger): We use Moving Average Convergence Divergence to pinpoint acceleration. Just because a stock is in an uptrend doesn't mean we should buy it today. The MACD tells us exactly when bullish momentum is picking up, acting as our precise entry trigger.

20-Day SMA (The Trailing Stop): We use a fast, 20-day moving average as our exit signal. Instead of guessing where the top is, we just follow the price up closely with this line. The moment the price breaks below it, we know the short-term trend is dead, and we lock in our profits.

Why we sidelined RSI and Bollinger Bands: You will notice we still calculate RSI and Bollinger Bands, but we removed them from our final Buy/Sell logic. Why? Because during testing, we realized these indicators were forcing us to take profits too early. Explosive, high-performing assets often stay "overbought" (high RSI) or ride the Upper Bollinger Band for months. By removing them from the strict logic, we stopped choking our winners.

Part 3: Why We Chose This Specific Strategy
The final strategy we deployed is known as Trend-Following Momentum.

Initially, we built a mean-reversion strategy that bought dips and sold quickly when the price popped. While this gave us a great win rate and almost zero drawdown, it resulted in a terrible overall return (only ~11% over 5 years). We were suffering from massive opportunity cost, sitting in cash while the asset went on a 400% run.

We pivoted to the Trend-Following strategy to solve this. The philosophy is simple: Cut your losses early, and let your winners run.

High Market Exposure: By relaxing the entry rules, the algorithm buys into major trends earlier and stays invested longer.

Asymmetrical Payoffs: We know that roughly 46% of our trades will be small losses (which is perfectly fine), but the remaining 54% of our trades will be massive winners that ride the trend upward for weeks or months. This is how we captured that 120% total return and crushed the broader market benchmark.

Part 4: How We Manage the Risk
Because a trend-following strategy inherently experiences a bit more volatility, we implemented two heavy layers of institutional risk management:

The Quarter-Kelly Bet (4.25%): The math told us that our statistical edge was so good we could theoretically bet ~17% of our capital per trade. We actively chose to ignore that and cut it down to a "Quarter-Kelly" (4.25%). Why? Because historical backtests are never perfectly accurate predictors of the future. By heavily penalizing our bet size, we ensure that even if the algorithm hits an unexpected losing streak in the real world, the portfolio survives.

Beta Hedging: We calculated that our asset is about 21% more volatile than the benchmark index (Beta of 1.21). If the entire stock market crashes tomorrow, our asset will likely crash even harder. By calculating the exact hedge ratio, we know exactly how much of the broader market index to short. This makes our portfolio "market-neutral"—meaning our profits come strictly from the algorithm's intelligence, regardless of whether the global economy is going up or down.
