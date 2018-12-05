import pandas as pd
import numpy as np

df_cars = pd.read_csv('cars.csv')
df_cars.head()

print(df_cars.columns)

print(df_cars.pivot_table(values='(kW)',index='YEAR',columns='Make',aggfunc=[np.mean,np.max]))

