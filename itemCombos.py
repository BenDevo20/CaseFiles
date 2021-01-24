import pandas as pd
import datetime as dt 
from datetime import timedelta
import numpy as np
from lmfit import Model
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
# import apyori as apriori
from mlxtend.frequent_patterns import apriori

df_all = pd.read_csv('DayPart.csv')
df_all['cnt']=1
scan_common = df_all.groupby('Scancode').sum()
scan_common = scan_common.loc[scan_common['cnt']>99]
scan_common = scan_common.reset_index()
codes = scan_common['Scancode'].unique()
trans = df_all['TransID'].unique()
df_all = df_all.loc[df_all['Scancode'].isin(codes)]
df_pairs = pd.DataFrame()
df_pairs['TransID']=trans
df_pairs[codes]=0
df_pairs = df_pairs.set_index('TransID')
cnt=0
for i, group in df_all.groupby('TransID')['Scancode']:
    for row in group:
        df_pairs[row][cnt] = 1
    cnt+=1

# df_pairs = df_pairs.reset_index()
df_temp = pd.DataFrame()
df_temp = [codes]
for index, row in df_pairs.iterrows():
    if row.sum() > 1:
        df_temp.append(row)
df_temp = pd.DataFrame(df_temp)
codes = df_temp.iloc[0]
df_temp.columns = df_temp.iloc[0]
df_temp.drop(0, inplace=True)
df_pairs = df_temp
# for i in codes:
    # df_pairs.loc[df_pairs[i]==1, i] = i

# records = []
# for i in range(0, len(df_pairs)):
    # records.append([str(df_pairs.values[i,j]) for j in range(0,len(codes))])
    
# for i in range(0,len(records)):
    # records[i] = [s.upper() for s in records[i] if s != '0']
    
# asso = list(map(frozenset, df_pairs))

asso_rules = apriori(df_pairs, use_colnames=True, min_support = .01)
for i in range(0,len(asso_rules)):
    asso_rules['itemsets'][i] = list(asso_rules['itemsets'][i])
    
asso_rules = pd.DataFrame(asso_rules)

descr = df_all.groupby('Scancode').first()
descr = descr.reset_index()
descr = descr[['Scancode','Description']]


for row in asso_rules['itemsets']:
    print('\n')
    print(descr.loc[descr['Scancode'].isin(row),'Description'])