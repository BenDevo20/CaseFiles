import pandas as pd
import datetime as dt 
from datetime import timedelta
import numpy as np
from lmfit import Model
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from mlxtend.frequent_patterns import apriori

df_all = pd.read_csv('DayPart.csv')
df_all['cnt']=1
df_all['Category'] = df_all['Category'].str.lower()
df_all['Description'] = df_all['Description'].str.lower()
beverages = ['carbonated soft drinks', 'coffee', 'sport drinks', 'energy drinks', 'juice/juice drinks', 'water']
df_all.loc[df_all['Category'].isin(beverages), 'Scancode'] = df_all['Category']
df_all.loc[df_all['Category'].isin(beverages), 'Description'] = df_all['Category']
df_all.loc[df_all['Description'].str.contains('belvita', na=False)==1, 'Scancode'] = 'belvita'
df_all.loc[df_all['Description'].str.contains('belvita', na=False)==1, 'Description'] = 'belvita'
scan_common = df_all.groupby('Scancode').sum()
scan_common = scan_common.loc[scan_common['cnt'] > 99]
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

asso_rules = apriori(df_pairs, use_colnames=True, min_support = .005)
for i in range(0,len(asso_rules)):
    asso_rules['itemsets'][i] = list(asso_rules['itemsets'][i])
    
asso_rules = pd.DataFrame(asso_rules)

descr = df_all.groupby('Scancode').first()
descr = descr.reset_index()
descr = descr[['Scancode','Description']]

combos = pd.DataFrame()
combo_list = []
for row in asso_rules['itemsets']:
    group = descr.loc[descr['Scancode'].isin(row),'Description']
    for i in group:
        combo_list = combo_list + [i]
    combo_list = [combo_list]
    combos = combos.append(combo_list)
    combo_list = []
combos.columns = ['Item1','Item2','Item3']
combos = combos.loc[combos['Item2'].isnull()==0]
combos.to_csv('combos.csv', index=False)

