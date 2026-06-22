## Week 1
I have included both the concepts that I've learnt from Week 1 and the assignments(reading/coding) given for week 1 here

### Concepts that I've learnt during the Week 1
## 1. What is a time series ?
A time series is simply a sequence of data points indexed in chronological order: $X_t$ for $t \in \{1, 2, \dots, T\}$.Examples include a company’s quarterly sales, daily stock returns, or monthly currency exchange rates. 
Unlike standard cross-sectional data, time-series observations are inherently dependent on their own past.
## 1.1 Why it matters in finance ?

Most financial data naturally appears as a time series. Stock prices, returns, volatility, interest rates, trading volume, and exchange rates all evolve over time.

Time series analysis helps answer some of the most important questions in quantitative finance:

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

**Example:** Stock market prices. Today's price is the baseline for tomorrow. If bad news drops a stock by 10% today, tomorrow's trading starts from that lower price.
## 2.3 Seasonality

Time series may follow recurring patterns at fixed intervals, such as daily, weekly, or yearly, due to seasonal effects.

## 2.4 Seasonality vs Cyclical behavior

**Cyclical behavior** refers to fluctuations in data (ups and downs) that occur over an extended, variable period—usually stretching across several years—driven by broader economic, political, or business conditions.

#### The Major Difference

- **Seasonality** happens at **fixed, predictable intervals within a year** (e.g., ice cream sales spiking every summer). You can circle the exact time it will happen on a calendar.
- **Cyclical behavior** happens over **unpredictable, varying lengths of time across multiple years** (e.g., an economic recession or housing market crash). You know it will happen eventually, but you cannot predict the exact year or duration.

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

There are a number of ways to test if your time series is stationary:

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

### Assignment(Reading/Coding)
## Chapter 2 From Ernie Chan's Book
## 1. Stationarity
The entire foundation of mean-reversion trading rests on finding a stationary time series.A time series is considered mathematically stationary if its core statistical properties—specifically its mean (average price) and variance (volatility)—remain constant over time.If you are trading a truly stationary asset, the strategy is perfectly clear:When the price deviates significantly above the mean, you short it.When the price deviates significantly below the mean, you buy it.The problem is that individual stock prices are not stationary. They generally follow a random walk (specifically, Geometric Brownian Motion) with an upward drift. Because individual stocks wander aimlessly, you cannot confidently say they will ever return to their historical average. Therefore, you need mathematical tools to prove whether a series is stationary before you risk money on it.
## 2. Tests for Stationarity:
The ADF TestTo scientifically determine if a time series is stationary (mean-reverting) or a random walk, quants use the Augmented Dickey-Fuller (ADF) test.The ADF test looks at the change in price from one period to the next ($\Delta y_t$) and tests if it is proportional to the difference between the current price and its mean. The core regression model looks like this:$$\Delta y_t = \lambda y_{t-1} + \mu + \beta t + \alpha_1 \Delta y_{t-1} + \dots + \epsilon_t$$The Logic: If the series is mean-reverting, the change in price ($\Delta y_t$) should be negative when the current price ($y_{t-1}$) is high, and positive when the current price is low. Therefore, the coefficient $\lambda$ must be negative.The Null Hypothesis: The ADF test assumes the series is a random walk ($\lambda = 0$).The Result: The test outputs a test statistic and a $p$-value. If the $p$-value is very small (typically $< 0.05$), you reject the null hypothesis. This gives you $95\%$ statistical confidence that the series is stationary.
## 3. Categorizing the Series using Hurst Exponent
While the ADF test gives a "yes or no" answer to stationarity, the Hurst Exponent ($H$) provides a continuous measure of a time series' "memory" and helps categorize its behavior.It is based on the idea that the variance of a random walk scales linearly with time ($\text{Var} \propto \tau$), while a trending or mean-reverting series scales differently ($\text{Var} \propto \tau^{2H}$).By calculating $H$, you can classify any market or asset:$H = 0.5$ (Random Walk): The series has no memory. Price movements are completely independent of past movements.$H < 0.5$ (Mean-Reverting / Anti-persistent): The series has a memory that forces it back to the mean. A positive move is statistically likely to be followed by a negative move.$H > 0.5$ (Trending / Persistent): The series has momentum. A positive move is statistically likely to be followed by another positive move.
## 4. The Half-Life of Mean Reversion
Identifying a stationary series is useless if it takes a decade for the price to revert to its mean. You need to calculate the half-life—the expected time it takes for the price to return exactly halfway to its historical average.Chan uses the continuous-time Ornstein-Uhlenbeck process to model this. By running a linear regression of the price changes against the lagged prices, you find the slope/coefficient ($\lambda$). You then plug $\lambda$ into the half-life formula:$$t_{1/2} = \frac{-\ln(2)}{\lambda}$$Why it is crucial: The half-life dictates your holding period. If $t_{1/2}$ is 5 days, it is a highly actionable strategy. If $t_{1/2}$ is 250 days, the capital requirement and opportunity cost are too high, and the structural "regime" of the market will likely change before you can exit the trade profitably.
## 5. Creating Stationarity using Cointegration
Because individual stocks are non-stationary, quants engineer their own stationary series using a concept called Cointegration.Cointegration occurs when two or more non-stationary time series (random walks) can be combined linearly to create a new, perfectly stationary time series.Example: Stock A and Stock B might both be wandering aimlessly. But if you calculate Stock A - (Hedge Ratio * Stock B), that resulting spread might be perfectly flat and stationary over time.Correlation vs. Cointegration: Chan emphasizes never confusing these two. Correlation means two stocks move in the same direction on a daily basis (returns). Cointegration means the distance between their absolute prices remains stable over the long term (prices). You trade cointegration, not correlation.
## 6. Testing for Cointegration
Chan outlines two primary methods for finding cointegrated assets:A. The CADF Test (For Pairs)When dealing with exactly two assets, you use the Cointegrating Augmented Dickey-Fuller (CADF) test.Run a linear regression between Asset A and Asset B. The slope of this regression is your hedge ratio.Calculate the residuals (the spread) using that hedge ratio.Run the standard ADF test on those residuals. If the residuals are stationary, the two assets are cointegrated.B. The Johansen Test (For Portfolios)When testing three or more assets (e.g., trying to cointegrate a basket of 5 tech stocks), CADF is insufficient. You must use the Johansen Test.It utilizes eigenvalues to determine how many stationary linear combinations (cointegrating vectors) exist within a larger portfolio.If you have $n$ assets in a basket, the Johansen test can identify up to $n-1$ different cointegrating relationships, allowing for complex, multi-leg statistical arbitrage portfolios.Would you like to see how to actually implement one of these mathematical models—like the Johansen Test or calculating the Half-Life—using Python code?



