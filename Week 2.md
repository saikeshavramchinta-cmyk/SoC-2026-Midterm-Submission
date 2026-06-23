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
In purely theoretical, continuous linear mean-reversion models, a strategy dictates that your position size should be directly proportional to how far the price has deviated from its mean.

While mathematically elegant, this is practically impossible to execute. It requires:

Constant, Infinitesimal Rebalancing: You would have to constantly buy or sell tiny fractions of shares every second as the price fluctuates.

Unlimited Capital: If the spread diverges to infinity, the linear model dictates you must keep buying all the way down, requiring infinite capital.

## 2. The Bollinger Band Solution
Bollinger Bands solve this implementation problem by transforming a continuous mathematical model into a system with discrete entry and exit thresholds. This allows a trader to hold distinct units of a portfolio (e.g., being fully "long," "short," or "flat" in one unit) rather than fractions of shares.

### How It Works Mechanically
To implement this, you calculate a moving average of the spread (or price ratio) and the standard deviation of that spread over a specific lookback period.
You then define specific thresholds based on the Z-score (the number of standard deviations the current price is away from the moving average).

The Entry Z-Score: You set a threshold to trigger a trade. For example, if the entryZscore is 2, you:

Go Short: When the price crosses above the Upper Band (Moving Average + 2 Standard Deviations).

Go Long: When the price crosses below the Lower Band (Moving Average - 2 Standard Deviations).

The Exit Z-Score: You set a threshold to close the trade. Usually, traders do not wait for the price to hit the opposite band. Instead, they set the exitZscore near 0.

Exit: You close out your long or short position as soon as the price reverts back to the Moving Average (or a small threshold near it, like 0.5 standard deviations).

## Capital Efficiency and Risk
Because Bollinger Bands restrict you to discrete states (you are either in the trade or out of the trade based on the bands), you eliminate the massive transaction costs of continuous rebalancing. It also caps your exposure, as you allocate a fixed unit of capital once the entry threshold is breached, preventing the "infinite capital" problem of purely linear scaling
## 3. Does Scaling-In actually work?
## The Flaw in the Math:
The primary weakness of the "all-in" mathematical proof is its reliance on a static universe. It operates on the implicit assumption that the probability of a price deviating further—and therefore the overall market volatility—remains perfectly constant over time.
## Dynamic Market Volatility:
In live financial markets, volatility is rarely constant, and the probabilities of deviation and reversion fluctuate constantly.
## The Conclusion:
Because real-world market volatility and probabilities change continuously, scaling-in frequently outperforms the "all-in" method in live, out-of-sample trading. While it may look sub-optimal in a rigid historical backtest, scaling-in remains a highly effective way to navigate the unpredictability of live markets and will likely yield a better realized Sharpe ratio.
## 4. Kalman Filter as Dynamic Linear Regression
The Kalman filter is the tool that tracks hidden, time-varying quantities in real time, updating its estimates as new data arrives.
Think of it this way - you are trying to track the “true” price of an asset but every observation you receive is the true price + noise. 
You cannot observe the true price directly - what you can do is maintain a running estimate of it and update that estimate each time a new noisy observation arrives - weighing up how much u trust the new data vs how much u trust your prior.
## 4.1 The Kalman filter in one sentence : 
A recursive algorithm that produces the optimal estimate of an unobservable state, given noisy observations by constantly balancing prior belief against new evidence.
## 4.2 How does it relate Mathmatically?
Mathematically the Kalman Filter is simply a state estimator - it is not a trading strategy.
The Kalman filter in principle takes your current prediction of that variable, take the new noisy measurement and blends them into the best estimate of what the variable actually is, weighing each one by how much you trust it. 
## 4.3 Why do quant firms need estimators ?
Funds use estimators - but not as an edge. They sit inside pipelines as the piece that estimates a hidden quantity. Estimating the variable is not a strategy - the strategy is what you do with the estimate.
Markets have very little signal relative to noise - and that is why even advanced estimators like particle filters and KalmanNet cannot really provide an edge because none of them is a strategy either. And no estimator, however modern can really pull out a signal that’s not there.
Every Kalman filter problem is written in two equations : 

1. **State equation** — describes how the hidden state evolves over time:

αₜ = Fαₜ  ₋  ₁ + Qηₜ ,    ηₜ ~ i.i.d. N(0, I)

2. **Observation equation** — describes how the observable data relates to the hidden state:

Yₜ = Hαₜ + Rεₜ  ,    εₜ ~ i.i.d. N(0, I)

<aside>
Where:
- `αₜ` is the state vector — the unobservable quantity you want to track (e.g. a time-varying hedge ratio, a latent factor, the output gap)  
- `Yₜ` is the observation vector — what you actually see in the data  
- `F` is the transition matrix — governs how the state evolves
- `H` is the observation matrix — maps the hidden state to observables
- `Q` and `R` are covariance matrices for state noise and observation noise respectively

## 4.4 The Filter : Two steps repeated forever

The Kalman filter runs the same two-step cycle at every time period.

**Step 1 — Predict.** 
Before observing `Yₜ`, use the state equation to project forward from last period's estimate:

αₜ|ₜ ₋  ₁ = F αₜ  ₋  ₁|ₜ ₋ ₁                         (predicted state)
Pₜ|ₜ  ₋  ₁ = F Pₜ  ₋  ₁|ₜ  ₋  ₁ Fᵀ + Q             (predicted covariance)

$P_{t|t-1}$ is your uncertainty about the state before seeing new data. Each prediction step increases uncertainty slightly — because the state may have moved since last period.
The notation `αₜ₋₁|ₜ₋₁` is just a way of saying - “my estimate of the state at time t-1, given all information available up to time t-1”

**Step 2 — Update.** 
Once `Yₜ` arrives, correct the prediction using the new information:

vₜ = Yₜ − H αₜ|ₜ₋₁                           (innovation — prediction error)
Sₜ = H Pₜ|ₜ  ₋  ₁ Hᵀ + R                     (innovation covariance)
Kₜ = Pₜ|ₜ ₋ ₁ Hᵀ Sₜ⁻¹                          (Kalman gain)

αₜ|ₜ = αₜ|ₜ ₋ ₁ + Kₜ vₜ                        (updated state estimate)
Pₜ|ₜ = (I − Kₜ H) Pₜ|ₜ  ₋  ₁                    (updated covariance)

The **innovation** `vₜ` is the surprise — how far the new observation was from what you predicted. 

The **Kalman gain** `Kₜ` determines how much weight to put on that surprise versus sticking with the prior prediction. It is automatically computed from the relative sizes of state uncertainty and observation noise.
## Interpretation of the Kalman Gain

$$
K_t=\frac{P_{t|t-1}H_t^T} {(H_tP_{t|t-1}H_t^T + R_t \ )}
$$

A closer look tells us that this is simply the ratio of **(how linked the state & observation is)** and **(the total uncertainty in the observation)**


### $$When \ R_t\to 0 \ (noiseless \ measurement), \ K_t \to H_t^{-1} \ and \ we \ trust \ the \ observation \ completely$$.
### $$When \ Q_t \to 0 \ (frozen \ state),  \ K_t \to 0 \ and \ we  \ trust  \ the \ prior \ completely$$.

For example -

If your quote comes from a deep-liquid exchange (low measurement noise) and your prior was already uncertain (high $P_t|t-1$) - the gain becomes large - 
signal :  move aggressively towards the new quote. 

If the quote instead comes from a thinly traded OTC desk (noisy instrument) and your model was already pretty confident (low $P_{t|t-1}$) - the gain becomes small - 
signal : stick with your prior - barely move.
The Kalman gain is the filter automatically doing this cost - benefit calculation at every single time step - no human judgement required.
## Kalman Filter as Market-Making Model
There is another noteworthy application of Kalman filter to a meanreverting strategy. In this application we are concerned with only one mean-reverting price series; we are not concerned with finding the hedge ratio between two cointegrating price series. However, as before, we still want to fi nd the mean price and the standard deviation of the price series for our mean reversion trading. So the mean price m(t) is the hidden variable here, and the price y(t) is the observable variable. The measurement equation in this case is trivial:
 y(t) = m(t) + ∋(t)  (“Measurement equation”)
with the same state transition equation
 m(t) = m(t − 1) + ω(t − 1). (“State transition”) (3.15)
So the state update equation 3.11 is just
 m(t | t) = m(t | t − 1) + K(t)( y(t) − m(t | t − 1)). (“State update”) (3.16)
(This may be the time to review Box 3.1 if you skipped it on fi rst reading.)
The variance of the forecast error is
 Q(t) = Var(m(t)) + Ve. (3.17)
The Kalman gain is
 K(t) = R(t | t − 1)/(R(t | t − 1) + Ve), (3.18)
and the state variance update is
 R(t | t) = (1 − K(t))R(t | t − 1). (3.19)
Example 3.3 (Continued)
Instead of coding the Kalman fi lter yourself as we demonstrated,
you can also use many free open-source MATLAB codes available.
One such package can be found at www.cs.ubc.ca/~murphyk
/Software/Kalman/kalman.html. Kalman fi lters are also available
from MATLAB’s Control System Toolbox.
83IMPLEMENTING MEAN REVERSION STRATEGIES
Why are these equations worth highlighting? Because this is a favorite
model for market makers to update their estimate of the mean price of an
asset, as Euan Sinclair pointed out (Sinclair, 2010). To make these equations
more practical, practitioners make further assumptions about the measurement error Ve, which, as you may recall, measures the uncertainty of the observed transaction price. But how can there be uncertainty in the observed
transaction price? It turns out that we can interpret the uncertainty in such
a way that if the trade size is large (compared to some benchmark), then the
uncertainty is small, and vice versa. So Ve in this case becomes a function of t
as well. If we denote the trade size as T and the benchmark trade size as Tmax,
then Ve can have the form
 Ve = R(t | t − 1) − ⎛
⎝
⎜ ⎞
⎠
⎟ T
T
1
max
(3.20)
So you can see that if T = Tmax, there is no uncertainty in the observed
price, and the Kalman gain is 1, and hence the new estimate of the mean
price m(t) is exactly equal to the observed price! But what should Tmax be? It
can be some fraction of the total trading volume of the previous day, for example, where the exact fraction is to be optimized with some training data.
Note the similarity of this approach to the so-called volume-weighted
average price (VWAP) approach to determine the mean price, or fair value
of an asset. In the Kalman fi lter approach, not only are we giving more
weights to trades with larger trade sizes, we are also giving more weights to
more recent trade prices. So one might compare this to volume and timeweighted average price.
