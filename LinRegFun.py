#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:10:29 2021

@author: bendevo20
"""
import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from scipy import stats 


# importing main sheet from excel
df_all = pd.read_csv('UnitSales.csv')

# dataframes by scancode number
scancode = df_all['Scancode'].unique()

df1 = df_all[df_all['Scancode']==scancode[0]]
df1.reset_index(inplace=True, drop=True)

df2 = df_all[df_all['Scancode']==scancode[1]]
df2.reset_index(inplace=True, drop=True)

df3 = df_all[df_all['Scancode']==scancode[2]]
df3.reset_index(inplace=True, drop=True)

# sum of all sales per product
sales = df1['SalesCount'].sum()
sales2 = df2['SalesCount'].sum()
sales3 = df3['SalesCount'].sum()
tot_sales = sales+sales2+sales3

proportions = np.round([[sales/tot_sales, sales2/tot_sales, sales3/tot_sales]],2)
print(proportions)
 
def regress_fun(df):
    
    # create model features
    X = np.array(df['Discount']).reshape(-1,1)
    y = np.array(df['SalesCount']).reshape(-1,1)
    
    
    # finding Z-score to identify outliers 
    zx = np.abs(stats.zscore(X))
    zy = np.abs(stats.zscore(y))
    
    """
    # remove outliers using quartile range 
    QuartX = np.percentile(X, [75, 25])
    Quarty = np.percentile(y, [75,25])
    
    X = df[(df['Discount'] >= QuartX[1]) & (df['Discount']) <= QuartX[0]]
    y = df[(df['SalesCount'] >= Quarty[1]) & (df['SalesCount']) <= Quarty[0]]
    """
         
    # create model 
    model = LinearRegression()
    model.fit(X,y)
    
    # model metrics
    test_pred = model.predict(X)
    residuals = y - test_pred
    MSE = mean_squared_error(y, test_pred)
    RMSE = np.sqrt(mean_squared_error(y, test_pred))
    
    return X, y, model, test_pred, residuals, MSE, RMSE

# regression functions for product vs discount values
reg1 = regress_fun(df1)
reg2 = regress_fun(df2)
reg3 = regress_fun(df3)

# creating subplots of products vs discount 
fig, axes = plt.subplots(nrows=1,ncols=3,figsize=(16,6))
# Product 1 sales vs discount 
axes[0].plot(reg1[0], reg1[1], 'o')
axes[0].plot(reg1[0],reg1[3],'o', color='red')
axes[0].set_ylabel('sales')
axes[0].set_title('28282')
# Product 2 sales vs discount
axes[1].plot(reg2[0], reg2[1], 'o')
axes[1].plot(reg2[0],reg2[3],'o', color='red')
axes[1].set_ylabel('sales')
axes[1].set_title('Other1')
# product 3 sales vs discount
axes[2].plot(reg3[0], reg3[1], 'o')
axes[2].plot(reg3[0],reg3[3],'o', color='red')
axes[2].set_ylabel('sales')
axes[2].set_title('other2')
plt.tight_layout()
plt.show()

