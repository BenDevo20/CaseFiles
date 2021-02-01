import pandas as pd
import pandas_datareader.data as wb
import datetime as dt 
from datetime import timedelta
import numpy as np
from numpy import exp, pi, sqrt
from lmfit import Model
import matplotlib.pyplot as plt
from tiingo import TiingoClient
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

Symbols = ['JNJ']
end = dt.datetime.now().date() - timedelta(days=2)
start = end - timedelta(days=1095)

mkt_all = pd.DataFrame()
for i in Symbols:
    data = wb.DataReader(i, 'yahoo', start, end)
    data.insert(0, 'Symbol', str(i))
    mkt_all = mkt_all.append(data)
    
mkt_all.reset_index(inplace=True)
mkt_all['Date'] = mkt_all['Date'].dt.date
mkt_all.set_index('Date', inplace=True)

df_cma = pd.DataFrame()
df_oma = pd.DataFrame()

for i in Symbols:
    
    df = mkt_all.loc[mkt_all['Symbol'] == i]
    
    cma_20 = df[['Close']].ewm(span=12).mean()
    cma_20.columns=['cma20']
    
    cma_50 = df[['Close']].ewm(span=26).mean()
    cma_50.columns=['cma50']
    
    
    oma_20 = df[['Open']].ewm(span=12).mean()
    oma_20.columns=['oma20']
    
    oma_50 = df[['Open']].ewm(span=26).mean()
    oma_50.columns=['oma50']
    

    dummy = pd.merge(cma_20, cma_50, on=['Date'])
    dummy = pd.merge(dummy, df['Close'], on=['Date'])
    dummy.insert(0, 'Symbol', str(i))
    
    dummy1 = pd.merge(oma_20, oma_50, on=['Date'])
    dummy1 = pd.merge(dummy1, df['Open'], on=['Date'])
    dummy1.insert(0, 'Symbol', str(i))
    
    df_cma = df_cma.append(dummy)
    df_oma = df_oma.append(dummy1)
    
df_cma['cma2050'] = df_cma['cma20'] - df_cma['cma50']
df_cma['cma2050_ema'] = df_cma['cma2050'].ewm(span=9).mean()

df_oma['oma2050'] = df_oma['oma20'] - df_oma['oma50']
df_oma['oma2050_ema'] = df_oma['oma2050'].ewm(span=9).mean()

df_cma.reset_index(inplace=True)
df_oma.reset_index(inplace=True)

df_cma = df_cma.set_index(['Date', 'Symbol'])
df_oma = df_oma.set_index(['Date', 'Symbol'])

scaler = MinMaxScaler()
df_cma[['Close', 'cma2050', 'cma2050_ema']] = scaler.fit_transform(df_cma[['Close', 'cma2050', 'cma2050_ema']])
df_oma[['Open', 'oma2050', 'oma2050_ema']] = scaler.fit_transform(df_oma[['Open', 'oma2050', 'oma2050_ema']])


df_cma.reset_index(inplace=True)
df_oma.reset_index(inplace=True)

plt.figure(figsize=(30, 9), dpi=100)
plt.plot(df_cma['Date'], df_cma['cma2050_ema'], 'b-', markersize=1.7, label='signal')
plt.plot(df_cma['Date'], df_cma['cma2050'], 'g-', markersize=1.7, label='12-26')
plt.plot(df_cma['Date'], df_cma['Close'], 'ro', markersize=1.7, label='close')
plt.legend()

plt.figure(figsize=(30, 9), dpi=100)
plt.plot(df_oma['Date'], df_oma['oma2050_ema'], 'b-', markersize=1.7, label='signal')
plt.plot(df_oma['Date'], df_oma['oma2050'], 'g-', markersize=1.7, label='12-26')
plt.plot(df_oma['Date'], df_oma['Open'], 'ro', markersize=1.7, label='open')
plt.legend()

