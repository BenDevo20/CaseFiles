#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 22:26:12 2021

@author: bendevo20
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# importing KioskImpressions to dataframe 
df_kiosk = pd.read_excel('Kiosk.xlsx')


# summing purchases and transactions by organization 
dfOrg = df_kiosk[['OrgAlias', 'Date', 'NetSales', 'Transactions']]

# aggregate transaction and net sales numbers per organization
dfOrgT = dfOrg.groupby('OrgAlias')['Transactions'].sum()
dfOrgT = dfOrgT.reset_index()
dfOrgS = dfOrg.groupby('OrgAlias')['NetSales'].sum()
dfOrgS = dfOrgS.reset_index()
# aggregate transaction and net sales numbers per organization per day
dfOrgDateS = dfOrg.groupby(['Date','OrgAlias'])['NetSales'].sum()
dfOrgDateS = dfOrgDateS.reset_index()
dfOrgDateT = dfOrg.groupby(['Date','OrgAlias'])['Transactions'].sum()
dfOrgDateT = dfOrgDateT.reset_index()
# merge agg data and dateagg data into dataframes
dfOrg = pd.merge(dfOrgT, dfOrgS, on='OrgAlias')
dfOrgDate = pd.merge(dfOrgDateT, dfOrgDateS, on=['OrgAlias','Date'])

# summing purchases and transaction by organization location 
dfLoc = df_kiosk[['LocAlias', 'Date', 'NetSales', 'Transactions']]
dfLocT = dfLoc.groupby('LocAlias')['Transactions'].sum()
dfLocT = dfLocT.reset_index()
dfLocS = dfLoc.groupby('LocAlias')['NetSales'].sum()
dfLocS = dfLocS.reset_index()
dfLoc = pd.merge(dfLocT, dfLocS,on='LocAlias')
# summing purchases and transaction by organization location per day
dfLoc = df_kiosk[['LocAlias', 'Date', 'NetSales', 'Transactions']]
dfLocDateT = dfLoc.groupby(['LocAlias','Date'])['Transactions'].sum()
dfLocDateT = dfLocDateT.reset_index()
dfLocDateS = dfLoc.groupby(['LocAlias', 'Date'])['NetSales'].sum()
dfLocDateS = dfLocDateS.reset_index()
# merge location and dated location transaction and netsales together
dfLoc = pd.merge(dfLocT, dfLocS, on='LocAlias')
dfLocDate = pd.merge(dfLocDateT, dfLocDateS, on=['LocAlias', 'Date']) 




# writing to CSV files 
dfOrg.to_csv('AggOrgData.csv')
dfOrgDate.to_csv('OrgDataDate.csv')
dfLoc.to_csv('AggLocData.csv')
dfLocDate.to_csv('LocDataDate.csv')
