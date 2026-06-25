# Overview of the Code implementation
My strategy is to implement three indicators(**MACD, RSI, Bollinger Bands**) and a **Volume Filter** together.
**I have added comments in the code for a better understanding of each and every line of code.**
The file **indicators.py** includes the code for the indicators.
The file **filters.py** includes the code for Volume Filter.
The file **signal_generator.py** includes the code required for the signal generation(Buy or Sell).
## Reason for using three indicators and a filter and how do they work together
## Spotting the Setup(Bollinger Bands)
We use Bollinger Bands to identify when price reaches an extreme low (hitting or piercing the lower band).
## Checking for Reversal Momentum(RSI):
We look at the RSI to verify if it is deeply oversold (below 30) or if the RSI is beginning to rise, which indicates weakening selling pressure.
## Validating the Trend Change(MACD): 
We wait for a bullish crossover on the MACD to confirm that the broader momentum is actually turning upwards rather than just experiencing a temporary bounce.
## Confirming with (Volume Filter):
We check if there is an expansion in trading volume coinciding with these signals. High volume confirms that buyers are stepping in heavily, giving us the green light to enter a trade with higher confidence.
### I have also implemented the code for Win Rate in the signal_generator.py to determine how well our strategy performs for a given dataset.
