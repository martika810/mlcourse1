import pandas as pd
import numpy as np

# df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
#
# for col in df.columns:
#     if col[:2]=='01':
#         df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
#     if col[:2]=='02':
#         df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
#     if col[:2]=='03':
#         df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
#     if col[:1]=='№':
#         df.rename(columns={col:'#'+col[1:]}, inplace=True)
#
# names_ids = df.index.str.split('\s\(') # split the index by '('
#
# df.index = names_ids.str[0] # the [0] element is the country name (new index)
# df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)
#
# df = df.drop('Totals')
# df.head()

# Q1
def answer_one():
    max = np.max(df['Gold'])
    return df[df['Gold']== max].index[0]

# q2
def answer_two():
    biggest_diff =np.max(df['Gold']-df['Gold.1'])
    return  df[df['Gold']-df['Gold.1'] == biggest_diff].index[0]

# Q3
def answer_three():
    cols_to_keep =['Gold','Gold.1','Gold.2']
    partial_data=df[cols_to_keep]
    partial_data=partial_data.where((partial_data['Gold']>0))
    partial_data=partial_data.where(partial_data['Gold.1']>0)
    partial_data['diff'] = (((partial_data['Gold']-partial_data['Gold.1'])*100)//(partial_data['Gold.2']))
    biggest_diff2=partial_data.dropna().sort_values(by='diff',ascending=False)
    return (biggest_diff2.index[0])


# Q4
def answer_four():
    s4=pd.Series(df['Gold.2']*3+df['Silver.2']*2+df['Bronze.2']*1,name='Points')
    return s4

################ PART 2 ######################
census_df = pd.read_csv('census.csv')
census_df.head()
# Q5

def answer_five():
    column_to_keep=['STNAME','CTYNAME']
    df1=census_df[column_to_keep]
    df1.set_index(column_to_keep)
    county_count_dataframe=df1.groupby('STNAME').count()
    max = np.max(county_count_dataframe['CTYNAME'])
    return county_count_dataframe[county_count_dataframe['CTYNAME'] == max].index[0]

# Q6
def answer_six():
    column_to_keep=['STNAME','CTYNAME','CENSUS2010POP']
    df2=census_df[column_to_keep].sort_values(by='CENSUS2010POP',ascending=False)
    return df2[1:4]['STNAME'].tolist()

# Q7
def answer_seven():
    estimated_columns = ['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012',
                         'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']
    cols_to_keep = ['SUMLEV','CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012',
                    'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']

    df4 = census_df[cols_to_keep]
    numeric_df=df4[estimated_columns]
    diff_dataframe=numeric_df.T.apply(lambda x: np.abs(np.subtract(np.min(x),np.max(x))))

    df4.iloc['diff'] = diff_dataframe
    df5 =df4.sort_values(by='diff',ascending=False)
    print(df5.iloc[0]['CTYNAME'])

# answer_seven()
# Q8
def answer_eight():
    cols_to_keep =['STNAME', 'CTYNAME']
    partial_data_8 =census_df.where(census_df['REGION']<3)
    partial_data_8 = partial_data_8.where(partial_data_8['CTYNAME'].str.startswith('Washington',na=False))
    partial_data_8 = partial_data_8.where(partial_data_8['POPESTIMATE2015']>partial_data_8['POPESTIMATE2014']).dropna()
    return (partial_data_8[cols_to_keep])


answer_eight()

