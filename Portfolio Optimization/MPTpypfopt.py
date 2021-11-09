# Non-pypfopt Libaries 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
from matplotlib.ticker import FuncFormatter

# Pypfopt Libaries 
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
from pypfopt import objective_functions


# Create Dataframe of Prices
tickers = ['VNQ','EEM','EFA','QQQ','SPY']
num_tickers = len(tickers)
price_data = []

for ticker in range(num_tickers):
    prices = web.DataReader(tickers[ticker], start='2020-01-01', end = '2021-10-10', data_source='yahoo')
    price_data.append(prices.assign(ticker=ticker)[['Adj Close']])
    df_stocks = pd.concat(price_data, axis=1)

df_stocks.columns  = tickers
#df_stocks.head()

"""
# Checking if any NaN values in the data
nullin_df = pd.DataFrame(df_stocks,columns=tickers)
print(nullin_df.isnull().sum())
"""
# Annualized Return
mu = expected_returns.mean_historical_return(df_stocks)

# Sample Variance of Portfolio
Sigma = risk_models.sample_cov(df_stocks)

# Weight bounds in negative allows shorting of stocks
ef = EfficientFrontier(mu, Sigma, weight_bounds=(0,1))  
fig, ax = plt.subplots()
plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)
plt.show()

#Max Sharpe Ratio - Tangent to the EF
ef = EfficientFrontier(mu, Sigma, weight_bounds=(0,1))  
ef.add_objective(objective_functions.L2_reg, gamma=2) # Adds penalty for not including assets 
ef.max_sharpe(risk_free_rate=0.02)
sharpe_pwt = ef.clean_weights()
print(sharpe_pwt)

