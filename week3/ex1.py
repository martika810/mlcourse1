import pandas as pd
import numpy as np

s = pd.Series(['Low', 'Low', 'High', 'Medium', 'Low', 'High', 'Low'])
s.astype('category', categories=['Low', 'Medium', 'High'], ordered=True)


s = pd.DataFrame(['Low', 'Low', 'High', 'Medium', 'Low', 'High', 'Low'])
s.rename(columns={0:'Levels'},inplace=True)

levels=s['Levels'].astype('category',categories=['Low','Medium','High'],ordered=True)
# print(levels)
# print(levels>'Low')
#
df =pd.read_csv('census.csv')
df =df[df['SUMLEV'] == 50]
df = df.set_index('STNAME').groupby(level = 0)['CENSUS2010POP'].agg({'avg':np.average})
pd.cut(df['avg'],10)

df_cars = pd.read_csv('cars.csv')
df_cars.head()
