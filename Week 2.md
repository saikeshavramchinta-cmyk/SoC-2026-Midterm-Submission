# Week 2

## Concepts that I've learnt
## Half-Life of Mean Reversion
We shall find another way to interpret the λ coefficient so that we know whether it is negative enough to make a trading strategy practical, even if we cannot reject the null hypothesis that its actual value is zero with 90 percent certainty in an ADF test. We shall find that λ is a measure of how long it takes for a price to mean revert.To reveal this new interpretation, it is only necessary to transform the discrete time series Equation to a differential form so that the changes in prices become infinitesimal quantities. Furthermore, if we ignore the drift (βt) and the lagged differences (Δy(t − 1), …, Δy(t − k)) in Equation **$$Δy(t) = λy(t − 1) + μ + βt + α_1Δy(t − 1) + … + α_kΔy(t − k) + ∋_t$$**, then it becomes recognizable in stochastic calculus as the Ornstein-Uhlenbeck formula for mean-reverting process:
### $$dy(t) = (λy(t − 1) + μ)dt + dε$$ 
where dε is some Gaussian noise. In the discrete form of **Δy(t) = λy(t − 1) + μ + βt + α1Δy(t − 1) + … + αkΔy(t − k) + ∋
t**, linear regression of Δy(t) against y(t − 1) gave us λ, and once determined, this value of λ carries over to the differential form of(**i.e Ornstein-Uhlenbeck formula**). But the advantage of writing the equation in the differential form is that it allows for an analytical solution for the expected value of y(t):
### $$E( y(t)) = y_0exp(λt) − μ/λ(1 − exp(λt))$$
Remembering that λ is negative for a mean-reverting process, this tells us that the expected value of the price decays exponentially to the value $−μ/λ$ with the half-life of decay equals to $−log(2)/λ$. First, if we find that λ is positive, this means the price series is not at all mean reverting, and we shouldn’t even attempt to write a mean reverting strategy to trade it. Second, if λ is very close to zero, this means the half-life will be very long, and a mean-reverting trading strategy will not be very profitable because we won’t be able to complete many round-trip trades in a given time period. Third, this λ also determines a natural time scale for many parameters in our strategy. For example, if the half life is 20 days, we shouldn’t use a look-back of 5 days to compute a moving average or standard deviation for a mean-reversion strategy. Often, setting the lookback to equal a small multiple of the half-life is close to optimal, and doing so will allow us to avoid brute-force optimization of a free parameter based on the performance of a trading strategy.

## Correlation(pitfall?)
A common pitfall in quantitative finance is assuming that two assets with a high correlation coefficient (like Pearson's 
ρ) can be traded as a mean-reverting pair. Correlation only measures the linear relationship between two variables over a specific time frame. Two tech stocks might both be trending upward in a bull market, yielding a correlation of 0.95. However, if their price difference (the spread) is not bounded, they can eventually diverge permanently, blowing up our account.

## Reading Assignment
## Chapter 3 from Ernie Chan's Book
## 1. Price Spreads vs. Log Price Spreads vs. Ratios
The mathematical representation of a portfolio spread dictates how it must be managed and executed:
### Price Spreads:
Formed via a weighted sum of raw prices ($y = y_1 - hy_2$). This fixes the literal share quantities of the components throughout the life of the trade.
### Log Price Spreads:
Cointegrates log-transformed price points ($log(q) = \sum h_i log(y_i)$). Here, weights represent fixed capital allocations. Because asset prices fluctuate, the trader must continuously rebalance the underlying shares to preserve these capital percentages, introducing heavy execution overhead and frictional costs.
### Ratios:
Trading a raw ratio ($y_1/y_2$) is highly practical for assets that lack absolute long-term cointegration but exhibit tight, short-term mean reversion. It naturally standardizes valuation across massive pricing shifts without demanding adaptive hedge calculations.
### The Problem with Theoretical Mean Reversion
In purely theoretical, continuous linear mean-reversion models, a strategy dictates that our position size should be directly proportional to how far the price has deviated from its mean.
While mathematically elegant, this is practically impossible to execute. It requires:
Constant, Infinitesimal Rebalancing: we would have to constantly buy or sell tiny fractions of shares every second as the price fluctuates.

Unlimited Capital: If the spread diverges to infinity, the linear model dictates we must keep buying all the way down, requiring infinite capital.

## 2. The Bollinger Band Solution
Bollinger Bands solve this implementation problem by transforming a continuous mathematical model into a system with discrete entry and exit thresholds. This allows a trader to hold distinct units of a portfolio (e.g., being fully "long," "short," or "flat" in one unit) rather than fractions of shares.

### How It Works Mechanically
To implement this, we calculate a moving average of the spread (or price ratio) and the standard deviation of that spread over a specific lookback period.
we then define specific thresholds based on the Z-score (the number of standard deviations the current price is away from the moving average).

The Entry Z-Score: we set a threshold to trigger a trade. For example, if the entryZscore is 2, we:

**Go Short:** When the price crosses above the Upper Band (Moving Average + 2 Standard Deviations).

**Go Long:** When the price crosses below the Lower Band (Moving Average - 2 Standard Deviations).

**The Exit Z-Score:** we set a threshold to close the trade. Usually, traders do not wait for the price to hit the opposite band. Instead, they set the exitZscore near 0.

Exit: we close out our long or short position as soon as the price reverts back to the Moving Average (or a small threshold near it, like 0.5 standard deviations).

## Capital Efficiency and Risk
Because Bollinger Bands restrict we to discrete states (we are either in the trade or out of the trade based on the bands), we eliminate the massive transaction costs of continuous rebalancing. It also caps our exposure, as we allocate a fixed unit of capital once the entry threshold is breached, preventing the "infinite capital" problem of purely linear scaling
## 3. Does Scaling-In actually work?
## The Flaw in the Math:
The primary weakness of the "all-in" mathematical proof is its reliance on a static universe. It operates on the implicit assumption that the probability of a price deviating further—and therefore the overall market volatility—remains perfectly constant over time.
## Dynamic Market Volatility:
In live financial markets, volatility is rarely constant, and the probabilities of deviation and reversion fluctuate constantly.
## The Conclusion:
Because real-world market volatility and probabilities change continuously, scaling-in frequently outperforms the "all-in" method in live, out-of-sample trading. While it may look sub-optimal in a rigid historical backtest, scaling-in remains a highly effective way to navigate the unpredictability of live markets and will likely yield a better realized Sharpe ratio.
## 4. Kalman Filter as Dynamic Linear Regression
The Kalman filter is the tool that tracks hidden, time-varying quantities in real time, updating its estimates as new data arrives.
Think of it this way - we are trying to track the “true” price of an asset but every observation we receive is the true price + noise. 
we cannot observe the true price directly - what we can do is maintain a running estimate of it and update that estimate each time a new noisy observation arrives - weighing up how much u trust the new data vs how much u trust our prior.
## 4.1 The Kalman filter in one sentence : 
A recursive algorithm that produces the optimal estimate of an unobservable state, given noisy observations by constantly balancing prior belief against new evidence.
## 4.2 How does it relate Mathmatically?
Mathematically the Kalman Filter is simply a state estimator - it is not a trading strategy.
The Kalman filter in principle takes our current prediction of that variable, take the new noisy measurement and blends them into the best estimate of what the variable actually is, weighing each one by how much we trust it. 
## 4.3 Why do quant firms need estimators ?
Funds use estimators - but not as an edge. They sit inside pipelines as the piece that estimates a hidden quantity. Estimating the variable is not a strategy - the strategy is what we do with the estimate.
Markets have very little signal relative to noise - and that is why even advanced estimators like particle filters and KalmanNet cannot really provide an edge because none of them is a strategy either. And no estimator, however modern can really pull out a signal that’s not there.
Every Kalman filter problem is written in two equations : 

1. **State equation** — describes how the hidden state evolves over time:

αₜ = Fαₜ  ₋  ₁ + Qηₜ ,    ηₜ ~ i.i.d. N(0, I)

2. **Observation equation** — describes how the observable data relates to the hidden state:

Yₜ = Hαₜ + Rεₜ  ,    εₜ ~ i.i.d. N(0, I)

<aside>
Where:
- `αₜ` is the state vector — the unobservable quantity we want to track (e.g. a time-varying hedge ratio, a latent factor, the output gap)  
- `Yₜ` is the observation vector — what we actually see in the data  
- `F` is the transition matrix — governs how the state evolves
- `H` is the observation matrix — maps the hidden state to observables
- `Q` and `R` are covariance matrices for state noise and observation noise respectively

## 4.4 The Filter : Two steps repeated forever

The Kalman filter runs the same two-step cycle at every time period.

**Step 1 — Predict.** 
Before observing `Yₜ`, use the state equation to project forward from last period's estimate:

αₜ|ₜ ₋  ₁ = F αₜ  ₋  ₁|ₜ ₋ ₁                         (predicted state)
Pₜ|ₜ  ₋  ₁ = F Pₜ  ₋  ₁|ₜ  ₋  ₁ Fᵀ + Q             (predicted covariance)

$P_{t|t-1}$ is our uncertainty about the state before seeing new data. Each prediction step increases uncertainty slightly — because the state may have moved since last period.
The notation `αₜ₋₁|ₜ₋₁` is just a way of saying - “my estimate of the state at time t-1, given all information available up to time t-1”

**Step 2 — Update.** 
Once `Yₜ` arrives, correct the prediction using the new information:

vₜ = Yₜ − H αₜ|ₜ₋₁                           (innovation — prediction error)
Sₜ = H Pₜ|ₜ  ₋  ₁ Hᵀ + R                     (innovation covariance)
Kₜ = Pₜ|ₜ ₋ ₁ Hᵀ Sₜ⁻¹                          (Kalman gain)

αₜ|ₜ = αₜ|ₜ ₋ ₁ + Kₜ vₜ                        (updated state estimate)
Pₜ|ₜ = (I − Kₜ H) Pₜ|ₜ  ₋  ₁                    (updated covariance)

The **innovation** `vₜ` is the surprise — how far the new observation was from what we predicted. 

The **Kalman gain** `Kₜ` determines how much weight to put on that surprise versus sticking with the prior prediction. It is automatically computed from the relative sizes of state uncertainty and observation noise.
## Interpretation of the Kalman Gain

$$
K_t=\frac{P_{t|t-1}H_t^T} {(H_tP_{t|t-1}H_t^T + R_t \ )}
$$

A closer look tells us that this is simply the ratio of **(how linked the state & observation is)** and **(the total uncertainty in the observation)**


### $$When \ R_t\to 0 \ (noiseless \ measurement), \ K_t \to H_t^{-1} \ and \ we \ trust \ the \ observation \ completely$$.
### $$When \ Q_t \to 0 \ (frozen \ state),  \ K_t \to 0 \ and \ we  \ trust  \ the \ prior \ completely$$.

For example -

If our quote comes from a deep-liquid exchange (low measurement noise) and our prior was already uncertain (high $P_t|t-1$) - the gain becomes large - 
signal :  move aggressively towards the new quote. 

If the quote instead comes from a thinly traded OTC desk (noisy instrument) and our model was already pretty confident (low $P_{t|t-1}$) - the gain becomes small - 
signal : stick with our prior - barely move.
The Kalman gain is the filter automatically doing this cost - benefit calculation at every single time step - no human judgement required.
## Kalman Filter as Market-Making Model
There is another noteworthy application of Kalman filter to a meanreverting strategy. In this application we are concerned with only one mean-reverting price series; we are not concerned with finding the hedge ratio between two cointegrating price series. However, as before, we still want to fi nd the mean price and the standard deviation of the price series for our mean reversion trading. So the mean price m(t) is the hidden variable here, and the price y(t) is the observable variable. The measurement equation in this case is trivial:
### y(t) = m(t) + ∋(t)  (“Measurement equation”)
with the same state transition equation
### m(t) = m(t − 1) + ω(t − 1). (“State transition”) 
So the state update equation 3.11 is just
### m(t | t) = m(t | t − 1) + K(t)( y(t) − m(t | t − 1)). (“State update”) (3.16)
(This may be the time to review Box 3.1 if we skipped it on fi rst reading.)
Th3e variance of the forecast error is
### Q(t) = Var(m(t)) + $V_e$
The Kalman gain is
### K(t) = R(t | t − 1)/(R(t | t − 1) + $V_e$), 
and the state variance update is
### R(t | t) = (1 − K(t))R(t | t − 1)
Why are these equations worth highlighting? Because this is a favorite model for market makers to update their estimate of the mean price of an asset, as Euan Sinclair pointed out (Sinclair, 2010). To make these equations more practical,
practitioners make further assumptions about the measurement error Ve, which, as we may recall, measures the uncertainty of the observed transaction price. But how can there be uncertainty in the observed transaction price? It turns out that we can interpret the uncertainty in such a way that if the trade size is large (compared to some benchmark), then the uncertainty is small, and vice versa. So Ve in this case becomes a function of t as well. If we denote the trade size as T and the benchmark trade size as Tmax, then Ve can have the form
### $V_e$ = ($R_{t|t-1}$)($(T/T_{max})-1$)
So we can see that if T = Tmax, there is no uncertainty in the observed price, and the Kalman gain is 1, and hence the new estimate of the mean price m(t) is exactly equal to the observed price! But what should Tmax be? It can be some fraction of the total trading volume of the previous day, for example, where the exact fraction is to be optimized with some training data.
**Note** the similarity of this approach to the so-called volume-weighted average price (VWAP) approach to determine the mean price, or fair value of an asset. In the Kalman fi lter approach, not only are we giving more weights to trades with larger trade sizes, we are also giving more weights to more recent trade prices. So one might compare this to volume and timeweighted average price.
## The Danger of Data Errors
### The Impact on Backtesting
Data errors fundamentally distort historical testing, but they affect different types of strategies in opposite ways.
Mean-Reverting Strategies (Inflated Profits): Errors and "outliers" typically artificially inflate the backtest performance of mean-reverting systems.
### Example:
If a stock's actual sequential trade prices are $100, $100, and $100, but a bad tick records them as $100, $110, and $100, a mean-reverting backtest will assume it successfully shorted the asset at $110 and covered at $100. This logs a fictitious $10 profit. Because intraday data contains vastly more quotes, the opportunity for these fake, profitable spikes is much higher.
### Momentum Strategies (Deflated Profits): 
Conversely, bad ticks usually suppress the backtest performance of momentum strategies.  Example: Using the same fake $110 spike, a momentum backtest would likely "buy" the breakout at $110, only to immediately get stopped out at the true $100 price, recording a fictitious loss. Because this understates rather than overstates performance, it is considered less dangerous than the illusions created in mean-reversion backtests.
### The Impact on Live Execution
While backtesting errors create illusions, live data errors create immediate financial losses for all types of strategies.
If a live data feed flashes an erroneous bid quote of $110, a trading algorithm might instantly fire a short market order to capture the anomaly.  However, because that $110 bid does not actually exist in the order book, the market order will simply execute at the true, lower market price (e.g., $100). This results in instant, unrecoverable slippage and real-world losses. 
### The Unique Vulnerability of Spread and Arbitrage Trading
Data errors are exceptionally dangerous when trading pairs or calculating spreads.
### The Math Behind the Risk:
Strategies rely on the difference between two quotes. Because a spread is usually a very small number compared to the absolute prices of the underlying assets, even a tiny data error results in a massive percentage distortion of the spread.
### Example:
Imagine Stock X has a true bid of $100 and Stock Y has a true ask of $105, making the true spread $5. If a data error causes Stock Y to display an ask of $106, the spread artificially jumps to $6. This $1 error represents a massive 20% increase in the spread's value, which is often more than enough to trigger an erroneous pair trade.
### Historical Data:
To prevent backtest manipulation, reputable data vendors use exchange-provided "cancel-and-correct" codes to filter out trades that executed too far from normal market prices.
### Live Data:
The author notes from personal experience that relying on standard broker data feeds for live equities pair-trading frequently triggered unexplained losing trades due to bad ticks. Switching to reliable third-party providers or institutional feeds (like Bloomberg) resolved the issue and stopped the erroneous trades.
