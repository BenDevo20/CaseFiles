#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:09:23 2021

@author: bendevo20
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn.metrics as metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# importing excel data
main_df = pd.read_csv('KioskImpressions.csv')

df = main_df.groupby('Discount').mean()
df = df.reset_index()

# creating X and Y values for regression
X = np.array(df['Discount']).reshape(-1,1)
y = np.array(df['SalesCount']).reshape(-1,1)

# creating regression model
model = LinearRegression()
model.fit(X, y)
test_pred = model.predict(X)
print(y, test_pred)
residuals = y - test_pred
MSE = mean_squared_error(y, test_pred)
print(MSE)
print(residuals)
