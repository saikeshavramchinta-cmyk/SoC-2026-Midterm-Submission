# Week 1
I have included both the concepts that I've learnt from Week 1 and the assignments(reading/coding) given for week 1 here

## Concepts that I've learnt during the Week 1
## 1. What is a time series ?
A time series is simply a sequence of data points indexed in chronological order: $X_t$ for $t \in \{1, 2, \dots, T\}$.Examples include a company’s quarterly sales, daily stock returns, or monthly currency exchange rates. 
Unlike standard cross-sectional data, time-series observations are inherently dependent on their own past.
## 1.1 Why it matters in finance ?

Most financial data naturally appears as a time series. Stock prices, returns, volatility, interest rates, trading volume, and exchange rates all evolve over time.

Time series analysis helps ans some of the most important questions in quantitative finance:

- How will a variable behave in the future?
- Is there an underlying trend or seasonal pattern?
- How volatile or risky is the series?
- How are multiple financial variables related over time?

# 2. Characteristics of Time Series

## 2.1 Trends

These are long-term movements in the data, showing a consistent rise or fall over time.

## 2.2 Deterministic vs Stochastic Trend

- Deterministic Trend (The Predictable Train)

A **deterministic trend** is a trend that changes at a constant, perfectly predictable rate over time. It follows a strict, pre-determined mathematical rule (like a straight line or a steady curve).

**Example:** Think of a company that adds exactly 500 new subscribers every single month, without fail.

- Stochastic Trend (The Random Wanderer)

A **stochastic trend** is a trend driven by random steps where the direction can shift unpredictably at any moment. "Stochastic" is just a fancy statistics word for "random."

**Example:** Stock market prices. Today's price is the baseline for tomorrow. If bad news drops a stock by 10% today, tomorrow's trading starts from that lo price.
## 2.3 Seasonality

Time series may follow recurring patterns at fixed intervals, such as daily, weekly, or yearly, due to seasonal effects.

## 2.4 Seasonality vs Cyclical behavior

**Cyclical behavior** refers to fluctuations in data (ups and downs) that occur over an extended, variable period—usually stretching across several years—driven by broader economic, political, or business conditions.

#### The Major Difference

- **Seasonality** happens at **fixed, predictable intervals within a year** (e.g., ice cream sales spiking every summer). We can circle the exact time it will happen on a calendar.
- **Cyclical behavior** happens over **unpredictable, varying lengths of time across multiple years** (e.g., an economic recession or housing market crash). We know it will happen eventually, but we cannot predict the exact year or duration.

## 2.5 Volatility

Some time series fluctuate significantly and unpredictably, with sharp changes in values over short periods.
## 2.6 **Non-linearity**

The relationship between time and the variable may not follow a straight line, making it challenging to capture with simple linear models.
## 3. Trend, Seasonal, Cyclical, Residual components

- **Trend:** The long-term upward or downward direction in the data over a prolonged period.
- **Seasonal:** Short-term fluctuations that repeat at fixed, predictable intervals within a year (e.g., daily, monthly).
- **Cyclical:** Long-term expansions and contractions that fluctuate over variable, unpredictable durations (usually multiple years).
- **Residual:** The random, erratic, and unpredictable "noise" left over after accounting for trend, seasonal, and cyclical patterns.
### What is Stationarity?
Stationarity is important because it implies that the statistical properties of the data generation process do not change over time - making it predictable.

#### 1. First-Order (or weak) Stationarity
It requires only that the expected value (mean) of the series remains constant over time:
$$\mathbb{E}[X_t] = \mu \quad \forall t$$
Note that the variance, skewness, and other higher moments can wildly drift. 

#### 2. Weak (Second-Order / Covariance) Stationarity
It requires that the mean and variance stay the same throughout, and the relationship between data points (that is autocovariance) is a function $\Delta{t}$ (how far apart they are in time, not when they occur.)
So, a process is weakly stationary if it satisfies three strict conditions:
1.  **Constant Mean:** $\mathbb{E}[X_t] = \mu$ for all $t$.
2.  **Finite Variance:** $\mathbb{E}[X_t^2] < \infty$ 
3.  **Time-Invariant Autocovariance:** 
$$\text{Cov}(X_t, X_{t+\tau}) = \gamma(\tau) \quad \text{where} \quad \Delta t = \tau$$

#### 3. Strict Stationarity
A process is strictly stationary if the entire *joint distribution* of any subsequence of data points remains completely invariant to time shifts. Formally, for any choice of $t_1, \dots, t_k$ and any shift $\tau$:
$$F_{X_{t_1}, \dots, X_{t_k}}(x_1, \dots, x_k) = F_{X_{t_1+\tau}, \dots, X_{t_k+\tau}}(x_1, \dots, x_k)$$
This implies that every single statistical moment (mean, variance, skewness, kurtosis, etc.) is a constant. 

In the real world, asset prices ($P_t$) are almost **never** stationary. They drift, trend, and explode. Therefore, our goal is rarely to find an inherently stationary asset, but rather to construct a stationary variation or combination of the series.

**Example!** 

Suppose the time series is:

$$
y_t = \beta_0 + \beta_1 t + \varepsilon_t
$$

This series is **not stationary** because the mean changes over time due to the trend component. Define a new series as:

$$
z_t = y_t - y_{t-1}
$$

Substitute the expressions for \(y_t\) and \(y_{t-1}\):

$$
z_t = (\beta_0 + \beta_1 t + \varepsilon_t) - (\beta_0 + \beta_1 (t-1) + \varepsilon_{t-1})
$$

$$
z_t = \beta_0 + \beta_1 t + \varepsilon_t - \beta_0 - \beta_1 t + \beta_1 - \varepsilon_{t-1}
$$

$$
z_t = \beta_1 + (\varepsilon_t - \varepsilon_{t-1})
$$

Since:

$$
E(\varepsilon_t) = 0
$$

then:

$$
E(z_t) = \beta_1
$$

Assuming the errors are independent:


Var($z_t$) = Var($\varepsilon_t - \varepsilon_{t-1}$) = $2\sigma^2$

Hence, using first differencing, this series is stationary.

## 4.How to check Stationarity of a time series?

There are a number of ways to test if our time series is stationary:

1. **Unit Root Tests**: Tests like the Augmented Dickey-Fuller (ADF) and Zivot-Andrews are used to see if the series has a unit root, which is a red flag for non-stationarity.
2. **KPSS Test**: This test works a bit differently - it checks if the series is stationary around a trend or needs differencing to become stationary.
3. **Run Sequence Plots**: A simple but effective visual method. These plots show the data over time and help spot trends or seasonal patterns.
4. **Less Common Tests**: There are more advanced methods like the Priestley-Subba Rao test or wavelet-based techniques, which are used in more specialised scenarios.
## 5. Methods to make a time series stationary
5.1 **Differencing (Fixes Shifting Mean) -** 

Tracks the **change** between periods to strip out stochastic trends (random walks).

- First-Order: $Y_t = X_t - X_{t-1}$ (removes linear trends)
- Second-Order: $Y't = Y_t - Y{t-1}$ (removes quadratic trends)
- Seasonal: $Y_t = X_t - X_{t-m}$ (removes cycles of period $m$, e.g., $m=12$)

5.2 **Detrending (Fixes Deterministic trends) -**

Used if data reverts to a predictable, constant path. Fit a trend line via regression and extract the stationary residuals:
                                     $Y_t = X_t - (\beta_0 + \beta_1 t)$

**Rule:** Use detrending for deterministic trends; use differencing for random walks.

5.3 **Log / Square Root Transformations (Fixes Changing Variance) -** 

Stabilizes **heteroscedasticity** (volatility that expands as the series value grows). *Apply before differencing.*

• **Log ( $\ln(X_t)$ ):** Flattens exponential growth and multiplicative variance.
• **Square Root ($\sqrt{X_t}$ ):** Stabilizes variance that scales proportionally to the mean.
## 6.Time Series Forecasting: ARIMA / SARIMA
ARIMA is one of the most widely used approaches to time series forecasting . These models focus on the autocorrelation structure of the series, that is, the dependence of observations on their past values. Before fitting an ARIMA model, the series must be stationary or transformed into a stationary series through differencing.  Stationarity is therefore a central requirement for ARIMA modeling.

An ARIMA model is built from three components, written as ARIMA (p,d,q) 
| Component | Symbol | Meaning |
| --- | --- | --- |
| **AR** (Autoregressive) |     p | Number of lagged values of the series used as predictors |
| **I** (Integrated) |    d | Number of times the series is differenced to achieve stationarity |
| **MA** (Moving Average) |    q | Number of lagged forecast errors used in the prediction |

## 6.1 Autoregressive (AR) component

In an autoregressive model of order p, the current value of the series depends linearly on its previous p values:

## $$y_t = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \dots + \phi_p y_{t-p} + \varepsilon_t$$


here,

- $y_t$ is current observation
- c is a constant
- $ϕ_1\;to\; ϕ_p$ are the autoregressive parameters
- $ϵ_t$ is white noise

An AR model resembles a regression on lagged values of the series itself. The coefficients $ϕ_i$ determine how strongly past observations influence the present.

- AR(0) with no constant corresponds to white noise, since the series contains only random shocks.
- AR(1) with $ϕ1$ = 1 and c = 0 is a random walk.
- AR(1) with $ϕ1$ = 1 and c ≠ 0 is a random walk with drift.
## 6.2 Moving Average (MA) component

A moving average model of order q uses past **forecast errors** in a regression-like model:


## $$y_t = c + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \dots + \theta_q \varepsilon_{t-q}$$


Here, the current value depends on previous error terms rather than past observations directly. The coefficients $θ_i​$ determines how past shocks propagate through time.

## 6.3 Integrated (I) component

The integrated component handles  non - stationary time series by differencing the series d times until stationarity is achieved.

Common cases include:

- d = 0: the series is already stationary
- d = 1: the first difference Y(t) - Y(t-1) is stationary
- d = 2: the second difference is stationary

In finance, asset prices are often non-stationary, while returns are typically closer to stationary.
### 6.4 General Equation for ARIMA

To write the model compactly, we use the backshift operator B, defined by:  Byₜ = yₜ₋₁

Combining all three factors , we get  : 


## $$(1 - \phi_1 B - \dots - \phi_p B^p)(1-B)^d y_t = c + (1 + \theta_1 B + \dots + \theta_q B^q)\varepsilon_t$$
## 6.5 SARIMA (Seasonal ARIMA) model

SARIMA extends ARIMA by incorporating seasonal patterns in the data. Seasonal differencing compares an observation with the corresponding observation from the previous season: $y_t - y_{t-s}$

This helps remove repeating seasonal patterns and makes the series more stationary before modeling.

A SARIMA model is represented as:

## $$\text{ARIMA}(p,d,q)(P,D,Q)_s$$

where:

- p,d,q are the non-seasonal autoregressive, differencing, and moving average orders
- P,D,Q are the seasonal autoregressive, differencing, and moving average orders
- s is the seasonal length
## Unit Root Tests:

Tests like the Augmented Dickey-Fuller (ADF) and Zivot-Andrews are used to see if the series has a unit root, which is a red flag for non-stationarity.

## Unit Roots - A gentle introduction

A unit root is a characteristic of a time series that makes it **non-stationary**.

When a time series has a unit root, it means its statistical properties (like variance) change over time. This is a problem because standard time series models (like AR, MA, ARMA) require the data to be stationary to make reliable predictions. If we model a non-stationary series without transforming it first, our results will likely be flawed.

## Example!

To understand unit roots mathematically, we can look at a simple Autoregressive model of order 1, or **AR(1)**. The formula for an AR(1) model is: $A_t = \phi A_{t-1} + \epsilon_t$

1. $A_t$: The value of the time series at time *t*
2. $A_{t-1}$: The value of the time series at the previous time step
3. $\phi$ **(phi)**: The coefficient (a multiplier) applied to the previous value
4. $\epsilon_t$: The error term (white noise) at time *t*, assumed to have a mean of 0 and a constant variance of $\sigma^2$
The entire concept of a unit root revolves around the value of this coefficient, $\phi$:

1. **Case 1:** $|\phi| < 1$ **(Stationary)**
If the absolute value of $\phi$ is less than 1 (e.g., 0.5, -0.7), the time series is **stationary**.
    1. **Expected Value (Mean):** As time goes on ($t \to \infty$), the expected value converges to 0
    2. **Variance:** The variance converges to a constant value: $\frac{\sigma^2}{1 - \phi^2}$ 
    
    Because both the mean and variance are constant over time, the series is stationary.
    
2. **Case 2:** $|\phi| > 1$ **(Explosive / Non-Stationary)**
If the absolute value of $\phi$ is greater than 1 (e.g., 1.5, -2), the time series is **non-stationary**
    1. **Expected Value (Mean):** The series will explode towards either positive or negative infinity as time progresses
    
    It clearly violates the constant mean assumption of stationarity.
    
3. $|\phi| = 1$ **(The Unit Root)**
If the absolute value of $\phi$ is exactly 1 (i.e., $\phi = \pm 1$ ), the time series has a **unit root**
    1. **Variance:** The variance at time *t* is $t \cdot \sigma^2$. This means that as time *t* increases, the variance grows larger and larger
    
    Because the variance is not constant and increases with time, a unit root process is **non-stationary**.
## Extending to any ARMA(p, q) model

With multiple $\phi$ coefficients, we use two key concepts which are the **Lag Operator** and the **Characteristic Equation**.

The Lag Operator (sometimes denoted as $B$ for Backshift) is a mathematical shortcut. When applied to a time series value, it shifts it back by one period.

1. $L \cdot Y_t = Y_{t-1}$
2. $L^2 \cdot Y_t = Y_{t-2}$
3. $L^p \cdot Y_t = Y_{t-p}$ and so on…

If we rewrite our AR(p) equation using the Lag Operator and move all the $Y$ terms to the left side, we get: $Y_t - \phi_1 L Y_t - \phi_2 L^2 Y_t - \dots - \phi_p L^p Y_t = \epsilon_t$
Factoring out $Y_t$ we get $(1 - \phi_1 L - \phi_2 L^2 - \dots - \phi_p L^p) Y_t = \epsilon_t$
To figure out if this complex model is stationary, mathematicians take the polynomial inside the parentheses, replace the Lag Operator ($L$) with a standard algebraic variable (usually $z$), and set it equal to zero. This is the **Characteristic Equation** of the time series $1 - \phi_1 z - \phi_2 z^2 - \dots - \phi_p z^p = 0$

The rule for stationarity depends entirely on where these roots fall relative to the unit circle:

This is literally where the term "Unit Root" comes from—it means that at least one of the roots (solutions for *z*) lies exactly on the unit circle (a magnitude of 1).

## Root location	$|z|$	Status
### Outside the circle	 $|z| > 1$	Stationary (The series is stable)
### Inside the circle	$|z| < 1$	Explosive (Non-stationary)
### Exactly ON the circle	$|z| = 1$	Unit Root (Non-stationary)

## Assignment(Reading/Coding)
## Chapter 2 From Ernie Chan's Book
## 1. Stationarity
The entire foundation of mean-reversion trading rests on finding a stationary time series.A time series is considered mathematically stationary if its core statistical properties—specifically its mean (average price) and variance (volatility)—remain constant over time.If we are trading a truly stationary asset, the strategy is perfectly clear:
### A.When the price deviates significantly above the mean, we short it.
### B.When the price deviates significantly below the mean, we buy it.
The problem is that individual stock prices are not stationary. They generally follow a random walk (specifically, Geometric Brownian Motion) with an upward drift. Because individual stocks wander aimlessly, we cannot confidently say they will ever return to their historical average. Therefore, we need mathematical tools to prove whether a series is stationary before we risk money on it.
## 2. Tests for Stationarity
To scientifically determine if a time series is stationary (mean-reverting) or a random walk, quants use the Augmented Dickey-Fuller (ADF) test.The ADF test looks at the change in price from one period to the next ($\Delta y_t$) and tests if it is proportional to the difference between the current price and its mean. The core regression model looks like this:
###  $\Delta y_t$ = $\lambda y_{t-1} + \mu + \beta t + \alpha_1 \Delta y_{t-1} + \dots + \epsilon_t$
### The Logic:
If the series is mean-reverting, the change in price ($\Delta y_t$) should be negative when the current price ($y_{t-1}$) is high, and positive when the current price is low. Therefore, the coefficient $\lambda$ must be negative.
### The Null Hypothesis:
The ADF test assumes the series is a random walk ($\lambda = 0$).
### The Result:
The test outputs a test statistic and a $p$-value. If the $p$-value is very small (typically $< 0.05$), we reject the null hypothesis. This gives us $95\%$ statistical confidence that the series is stationary.
## 3. Categorizing the Series using Hurst Exponent
While the ADF test gives a "yes or no" answer to stationarity, the Hurst Exponent ($H$) provides a continuous measure of a time series' "memory" and helps categorize its behavior.The Hurst Exponent modifies the standard variance equation by introducing a scaling exponent, $H$. It proposes that the variance of log prices scales proportionally to the time lag raised to the power of $2H$:
## $$\langle|z(t + \tau) - z(t)|^2\rangle \sim \tau^{2H}$$
### $H = 0.5$ (Random Walk):
The equation simplifies to $\tau^{1}$, confirming the asset diffuses at a normal, unpredictable rate.
### $H < 0.5$ (Mean-Reverting):
The variance grows slower than time. This indicates the series is "anti-persistent." If it goes up today, it is statistically more likely to go down tomorrow, keeping the long-term variance constrained.
### $H > 0.5$ (Trending):
The variance grows faster than time. The series is "persistent." A positive move today increases the likelihood of another positive move tomorrow, causing the price to drift further away from its origin.
## How it is calculated (Based on the MATLAB snippet):
To calculate $H$, the code (calculateHurstExponent.m) computes the variance of the price differences for various time lags ($\tau = 2, 4, 8, \dots, 100$). It then plots the $\log(\tau)$ against the $\log(\text{Variance})$. Because taking the logarithm of the formula above yields a linear equation ($y = 2H \cdot x + c$), running a simple linear regression on these log values yields a slope. Half of that slope is our Hurst Exponent.(Note: The book mentions an example where the USD.CAD pair yielded an $H$ of 0.49, indicating it is very weakly mean-reverting, almost a random walk).
## 4. The Variance Ratio Test
The Variance Ratio test approaches the exact same core concept from a slightly different mathematical angle. Instead of calculating an exponent, it calculates a direct ratio.It tests the null hypothesis that the variance of a multi-period return is simply proportional to the variance of a single-period return.
## $$\text{Variance Ratio} = \frac{\text{Var}(z(t) - z(t-\tau))}{\tau \cdot \text{Var}(z(t) - z(t-1))}$$
### Ratio $= 1$:
The series is a random walk.
### Ratio $< 1$:
The series is mean-reverting (the multi-period variance is smaller than a random walk would suggest).
### Ratio $> 1$:
The series is trending.
### Statistical Importance:
While the Hurst Exponent provides a measurement, the Variance Ratio is often used as a formal statistical test (often associated with Lo and MacKinlay's 1988 paper, as noted in the book). It allows quants to generate a test statistic and $p$-value to determine if they can confidently reject the random walk hypothesis. 
## 5. The Half-Life of Mean Reversion
Identifying a stationary series is useless if it takes a decade for the price to revert to its mean. We need to calculate the half-life—the expected time it takes for the price to return exactly halfway to its historical average.This book uses the continuous-time Ornstein-Uhlenbeck process to model this. By running a linear regression of the price changes against the lagged prices, we find the slope/coefficient ($\lambda$). We then plug $\lambda$ into the half-life formula:
 ### $t_{1/2}$ = $\frac{-\ln(2)}{\lambda}$
### Why it is crucial:
The half-life dictates our holding period. If $t_{1/2}$ is 5 days, it is a highly actionable strategy. If $t_{1/2}$ is 250 days, the capital requirement and opportunity cost are too high, and the structural "regime" of the market will likely change before we can exit the trade profitably.
## 6. A Linear Mean Reverting Trading Strategy
A linear mean-reverting strategy capitalizes on the tendency of a specific asset's price to return to its historical average over time. To execute this profitably, two foundational conditions must be met:
The price series must be demonstrably mean-reverting (stationary).The half-life of this mean reversion must be shorter than our required trading horizon.Once these conditions are satisfied, the trading mechanics follow a straightforward, linear set of rules.Calculating the SignalThe strategy relies on calculating the normalized deviation of the asset's current price from its moving average. This is effectively a Z-score, which measures how many standard deviations the current price is from the mean:
## $$\text{Normalized Deviation} = \frac{P_t - \mu}{\sigma}$$
### $P_t$ = Current Price
### $\mu$ = Moving Average over the look-back period
### $\sigma$ = Moving Standard Deviation over the look-back period
## Capital Allocation:
The number of units held in the asset should be negatively proportional to the normalized deviation. If the price spikes two standard deviations above the mean, we take a proportionately large short position. As the price falls back toward the mean, we scale out of the short.
## The Look-back Period:
The window used to calculate both the moving average ($\mu$) and the moving standard deviation ($\sigma$) is typically set equal to the calculated half-life of the asset's mean reversion.

## 7. Creating Stationarity using Cointegration
Because individual stocks are non-stationary, quants engineer their own stationary series using a concept called Cointegration.
### Cointegration:
Cointegration occurs when two or more non-stationary time series (random walks) can be combined linearly to create a new, perfectly stationary time series.
### Example:
Stock A and Stock B might both be wandering aimlessly. But if we calculate Stock A - (Hedge Ratio * Stock B), that resulting spread might be perfectly flat and stationary over time.
## Correlation vs. Cointegration:
Correlation means two stocks move in the same direction on a daily basis (returns). Cointegration means the distance between their absolute prices remains stable over the long term (prices). We trade cointegration, not correlation.
## 8. Testing for Cointegration
The book outlines two primary methods for finding cointegrated assets:
### A. The CADF Test (For Pairs)
When dealing with exactly two assets, we use the Cointegrating Augmented Dickey-Fuller (CADF) test.Run a linear regression between Asset A and Asset B. The slope of this regression is our hedge ratio.Calculate the residuals (the spread) using that hedge ratio.Run the standard ADF test on those residuals. If the residuals are stationary, the two assets are cointegrated.
### Find hedge ratio:
We run a regression to find the optimal ratio ($\beta$) to combine the two assets $P_A = \beta \times P_B$
### Test the residuals:
Check if the resulting spread ($= P_A - \beta \times P_B$) is stationary using ADF test. If it is the pair is cointegrated
### B. The Johansen Test (For Portfolios)
When testing three or more assets (e.g., trying to cointegrate a basket of 5 tech stocks), CADF is insufficient. We must use the Johansen Test.It utilizes eigenvalues to determine how many stationary linear combinations (cointegrating vectors) exist within a larger portfolio.If we have $n$ assets in a basket, the Johansen test can identify up to $n-1$ different cointegrating relationships, allowing for complex, multi-leg statistical arbitrage portfolios.

## $$\Delta Y(t) = \Lambda Y(t - 1) + M + A_1\Delta Y(t - 1) + \dots + A_k\Delta Y(t - k) + \epsilon_t$$
The core of the test revolves around the matrix $\Lambda$. If $\Lambda = 0$, the next move of $Y$ does not depend on the current price level, meaning there is no mean reversion and therefore no cointegration.Rank ($r$) and Portfolios:
Let $r$ denote the rank of the matrix $\Lambda$, and $n$ denote the total number of price series. The rank $r$ represents the exact number of independent portfolios that can be constructed using various linear combinations of these cointegrating price series.
## Test Statistics:
The test calculates the rank $r$ using eigenvector decomposition of $\Lambda$. This yields two distinct test statistics:
## The trace statistic.
### The eigen statistic
### Hypothesis Testing
We do not need to calculate the statistics manually; software packages provide the necessary critical values. The test evaluates a sequence of null hypotheses:$r = 0$ (indicating no cointegrating relationship exists)$r \le 1$... continuing up to $r \le n - 1$If the test allows we to reject all of these null hypotheses, we can conclude that $r = n$.
## Application of Johansen Test
## Hedge Ratios
As a highly useful byproduct of calculating these statistics, the eigenvectors discovered during the Johansen Test can be directly applied as hedge ratios. These ratios dictate how to weight the individual price series to successfully form a stationary, mean-reverting portfolio.
## 9. Pros and Cons of Mean-Reverting Strategies
## Pros
## Flexible Construction:
we are not restricted to instruments that are intrinsically stationary. we can select and combine various cointegrating stocks and ETFs to construct a custom stationary, mean-reverting portfolio.

## Trading Opportunities:
There is a many choices, aided by the continuous creation of new ETFs that offer marginally different exposures.

## Strong Fundamental Relationship:
Mean-reverting pairs usually have clear fundamental backing (e.g., pairing the Australian and Canadian economies because both are commodity-dominated, or pairing gold with gold-mining companies).

## Understandable Failures:
When a cointegrating pair breaks down, the underlying cause is typically identifiable (such as high energy prices disrupting the relationship between gold and gold miners). This contrasts with momentum strategies, which rely on the "greater fool" theory and can fail without clear explanation.

## Adaptable Time Scales:
These strategies can be applied across a wide spectrum of timeframes, ranging from seconds (market-making) to years (fundamental value investing).

## Favorable Statistics on Short Timeframes:
Operating on shorter time scales allows for a higher volume of trades annually. This leads to greater statistical confidence, higher Sharpe ratios, and higher compounded returns.

## Cons
The strategy's high consistency can lull traders into a false sense of security, often resulting in dangerous levels of overleverage (similar to the downfall of Long Term Capital Management).

## Catastrophic Risk:
When a mean-reverting strategy suddenly fails—often due to fundamental shifts only discernible in hindsight—it typically occurs precisely when the trader is operating at maximum leverage after a long winning streak. This makes the rare losses extremely painful and sometimes catastrophic.

## Difficult Risk Management:
Standard risk management techniques, such as traditional stop-losses, cannot logically be deployed in mean-reverting systems, making risk mitigation particularly challenging.

## Section 18.8 from Paul Wilmott on Quantitative Finance
## 1.Cointegration vs. Correlation
the book contrasts Cointegration with traditional models like Modern Portfolio Theory (MPT) and the Capital Asset Pricing Model (CAPM).
### Reliability
CAPM is generally considered more reliable than MPT because it relies on fe input parameters.
### The Flaw of Correlation:
Two stocks can be perfectly correlated in the short term but diverge entirely in the long run. Conversely, two stocks might have zero correlation but never wander too far apart from each other.
### The Use Case:
While short-term correlation is useful for strategies like delta hedging, cointegration is much more valuable when holding an unhedged portfolio over a long period.
## 2. The Concept of Stationarity
Stationary Series: A time series that has a finite and constant mean, standard deviation, and autocorrelation function. It essentially oscillates around a baseline and does not wander too far from its mean.
### Non-Stationary Series:
Standard stock prices tend to grow over time and are therefore non-stationary.The Coin-Tossing Analogy:
### Stationary Example:
The outcome of individual coin tosses (+1 for heads, -1 for tails) is stationary. It has a mean of 0 and a standard deviation of 1.
### Non-Stationary Example:
The cumulative sum of those coin tosses (like a running betting tally) is non-stationary. Even though the mean remains 0, the sum wanders further away from the baseline, and its standard deviation grows proportionally to the square root of the number of throws.
## 3. Mathematical Testing for Stationarity
Testing a time series $X_t$ involves finding coefficients ($a$, $b$, and $c$) using the following linear regression model:
## $$X_t = a X_{t-1} + b + ct$$
### The value of coefficient $a$ dictates the nature of the series:
### Unstable: $|a| > 1$
### Stationary: $-1 \le a < 1$
### Non-Stationary: $a = 1$
Because this relies on statistical probability, the book notes that the Dickey-Fuller statistic is required to determine the actual degree of confidence in the result.
## 4. Defining Cointegration in Portfolios
The book defines cointegration as the ability to combine non-stationary individual stocks into a stationary portfolio.Mathematically, we are looking for specific portfolio weights ($\lambda_i$) where the sum of the weights equals 1 ($\sum_{i=1}^{N} \lambda_i = 1$), such that the linear combination of the stock prices ($S_i$) results in a stationary series:
## $$\sum_{i=1}^{N} \lambda_i S_i$$
If we can find this stationary combination, the underlying stocks are considered cointegrated.
## 5. Practical Applications in Finance
### Index Tracking:
Instead of buying all 500 stocks in the S&P 500, we can find a smaller portfolio (e.g., 15 stocks) that is cointegrated with the index. Because it is cointegrated, the tracking error will have a constant mean and standard deviation, meaning it will reliably track the index without wandering off.
### Targeting Arbitrary Returns:
A trader doesn't have to track an index; they could track an exponential math curve like $e^{0.2t}$ to target a consistent 20% return.
### Pairs Trading:
Analyzing two related stocks (like Nike and Reebok) to find a cointegrated relationship that can be traded against one another.
### The Ultimate Advantage:
Unlike MPT and CAPM, cointegration does not require volatility and correlation to appear explicitly in the analysis, making it reliant on far fe assumed properties of individual time series.
