#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 16:08:25 2021

@author: bendevo20
"""

import pandas as pd
import datetime as dt 
from datetime import timedelta
import numpy as np
from numpy import exp, pi, sqrt
from lmfit import Model
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats

# correlation between price and sales count?

df_all = pd.read_csv('KioskImpressions.csv')
serials = df_all['Scancode'].unique()
org = df_all['OrgAlias'].unique()
loc = df_all['LocAlias'].unique()

def parse(df, parser):
    dict1 = {}
    for i in parser:
          df1 = df[df['Scancode']==i]
          df1['Price'] = df1['LocationItemPrice'] - df1['Discount']
          df1 = df1.groupby('Price').mean()
          df1 = df1.reset_index()
          df1 = df1.loc[np.abs(stats.zscore(df1['SalesCount']))<3]
          x = np.array(df1['Price']).reshape(-1,1)
          y = np.array(df1['SalesCount']).reshape(-1,1)
          model = LinearRegression()
          model.fit(x,y)
          yfit = model.predict(x)
          r2 = np.round(r2_score(y, yfit),4)
          dict1[i] = [x, y, yfit, r2]
    return dict1
dict1 = parse(df_all, serials)

for i in serials:
    x = dict1[i][0]
    y = dict1[i][1]
    yfit = dict1[i][2]
    r2 = dict1[i][3]
    plt.figure()
    plt.figtext(0,0, str('r-sq: ' + str(r2)),  style='italic', \
             bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    plt.scatter(x,y, label = 'actual')
    plt.plot(x,yfit, label = 'best fit')
    plt.legend(loc='best')
    
# Where are things sold, where are they popular, what is the least available product?

# Product sales as portion of total product sales
df_total = df_all.groupby('Scancode').sum()
for i in serials:
    df_all.loc[df_all['Scancode']==i, 'portion'] = df_all['SalesCount']/df_total['SalesCount'][i]
    
# Portion of product sales summed by Org
df_portion = df_all.groupby(['OrgAlias', 'Scancode']).sum()['portion']

for i, group in df_all.groupby('OrgAlias'):
    print('\n')
    for prod in serials:
        if prod in set(group['Scancode']):
            print(str(i) + ', ' + 'Item ' + str(prod) + ': ' + \
                  str(group.loc[group['Scancode']==prod]['SalesCount'].sum()))
            # Proportion of sales by org
