## Week 1
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
1. **Differencing (Fixes Shifting Mean) -** 

Tracks the **change** between periods to strip out stochastic trends (random walks).

- First-Order: $Y_t = X_t - X_{t-1}$ (removes linear trends)
- Second-Order: $Y't = Y_t - Y{t-1}$ (removes quadratic trends)
- Seasonal: $Y_t = X_t - X_{t-m}$ (removes cycles of period $m$, e.g., $m=12$)

2. **Detrending (Fixes Deterministic trends) -**

Used if data reverts to a predictable, constant path. Fit a trend line via regression and extract the stationary residuals:
                                     $Y_t = X_t - (\beta_0 + \beta_1 t)$

**Rule:** Use detrending for deterministic trends; use differencing for random walks.

3. **Log / Square Root Transformations (Fixes Changing Variance) -** 

Stabilizes **heteroscedasticity** (volatility that expands as the series value grows). *Apply before differencing.*

• **Log ( $\ln(X_t)$ ):** Flattens exponential growth and multiplicative variance.
• **Square Root ($\sqrt{X_t}$ ):** Stabilizes variance that scales proportionally to the mean.
