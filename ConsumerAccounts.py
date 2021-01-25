#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:27:39 2021

@author: bendevo20
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import sklearn 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# importing main data file 
df_kiosk = pd.read_excel('Kiosk.xlsx')

# sub dataframe for columns interested in consumer accounts 
dfConAcc = df_kiosk.drop(['Taxes', 'GrossSales', 'OrgAlias','Week No', 'Taxes', 'Items'], axis=1)

# summing transactions and consumer account transactions grouped by organization
dfRank = dfConAcc
dfRank = dfRank.groupby('LocAlias')[['Transactions', 'AccountPurchases']].sum()
dfRank['Acc/Trans'] = dfRank['AccountPurchases'] / dfRank['Transactions']
dfRank = dfRank.reset_index()
dfRank = dfRank.sort_values(by=['Acc/Trans'], ascending=True)
dfRank['Rank'] = 0

dfRank.loc[dfRank['Acc/Trans'] <= .2,'Rank'] = 1
dfRank.loc[(dfRank['Acc/Trans'] > .2) & (dfRank['Acc/Trans'] <= .4),'Rank'] = 2
dfRank.loc[(dfRank['Acc/Trans'] > .4) & (dfRank['Acc/Trans'] <= .6),'Rank'] = 3
dfRank.loc[(dfRank['Acc/Trans'] > .6) & (dfRank['Acc/Trans'] <= .8),'Rank'] = 4
dfRank.loc[dfRank['Acc/Trans'] > .8,'Rank'] = 5

dfConPur = dfConAcc
dfConPur = dfConPur.groupby('LocAlias')[['NetSales', 'ConsumerTotalEstimate']].sum()
dfConPur['AccPur/Sales'] = dfConPur['ConsumerTotalEstimate'] / dfConPur['NetSales']
dfConPur = dfConPur.reset_index()


"""
# regression of unique consumer accounts on NetSales 
X = np.array(dfConAcc['UniqueConsumerAccounts']).reshape(-1,1)
y = np.array(dfConAcc['NetSales']).reshape(-1,1)


# creating regression model
model = LinearRegression()
model.fit(X, y)
test_pred = model.predict(X)
residuals = y - test_pred
MSE = mean_squared_error(y, test_pred)
print(MSE)
print(residuals)
print(y, test_pred)

fig, axes = plt.subplots(nrows=1,ncols=1,figsize=(16,6))
# Product 1 sales vs discount 
#axes.plot(X, y, 'o')
axes.plot(y,test_pred,'o', color='red')
axes.set_ylabel('sales')
axes.set_title('Consumer Accounts')
plt.show()
"""
