#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 18:44:43 2021

@author: bendevo20
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 


# read in day part excel file 
df_main = pd.read_csv('DayPart.csv')

# Items bought together 
transID = df_main['TransID'].unique()


df1 = df_main[df_main['TransID']==transID[0]]
df1.reset_index(inplace=True, drop=True)
"""
for i in transID:
    transaction = df_main[df_main['TransID']==i].count()
  """

# time of day analysis per cateogry 
dfTime = df_main[['Hour','Date','Category']]
dfTime['Category'] = dfTime['Category'].str.upper()
dfTime['Count'] = 1
dfTime = dfTime.groupby(['Hour','Category'])['Count'].sum()
dfTime = dfTime.reset_index()

# Data frame of aggregate values from time dataFrame
dfAgg = pd.DataFrame()
# Average number of items bought at each time of day
dfAgg['HourAverage'] = dfTime.groupby('Hour')['Count'].mean()
# Total number of items bought at each time of day
dfAgg['HourCount'] = dfTime.groupby('Hour')['Count'].sum()

# Sales per category proportion of location (org and location)
dfOrgC = df_main[['Date', 'Category', 'Hour', 'OrgAlias']]
dfOrgC['Category'] = dfOrgC['Category'].str.upper()
dfOrgC['Count'] = 1
dfOrgC = dfOrgC.groupby(['OrgAlias','Category'])['Count'].sum()
dfOrgC = dfOrgC.reset_index()

# Sales per category proportion of location (org and location)
dfLocC = df_main[['Date', 'Category', 'Hour', 'LocAlias']]
dfLocC['Category'] = dfLocC['Category'].str.upper()
dfLocC['Count'] = 1
dfLocC = dfLocC.groupby(['LocAlias','Category'])['Count'].sum()
dfLocC = dfLocC.reset_index()
