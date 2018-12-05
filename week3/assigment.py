import pandas as pd

# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,
#
# e.g.
#
# 'Bolivia (Plurinational State of)' should be 'Bolivia',
#
# 'Switzerland17' should be 'Switzerland'.
#
#
#
# Next, load the GDP data from the file world_bank.csv, which is a csv containing countries'
#  GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.
#
# Make sure to skip the header, and rename the following list of countries:
#
# "Korea, Rep.": "South Korea",
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"
#
#
#
# Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx,
# which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.
#
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only
# the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
#
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', '
# Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006',
# '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
#
# This function should return a DataFrame with 20 columns and 15 entries.
def scimen():
    # Load ScimEn data and treat
    ScimEn = pd.read_excel("scimagojr-3.xlsx")
    # ScimEn = ScimEn.set_index(['Country'])
    return ScimEn

def gdp():
    # Load world bank data and treat them
    gdp=pd.read_csv('world_bank.csv')
    gdp = gdp[4:269]

    gdp = gdp.set_index(['Data Source'])
    gdp=gdp.rename(index={'Korea, Rep.':'South Korea',
                          'Iran, Islamic Rep.':'Iran',
                          'Hong Kong SAR, China':'Hong Kong'})
    gdp=gdp.rename(columns ={'Unnamed: 50':'2006','Unnamed: 51':'2007','Unnamed: 52':'2008','Unnamed: 53':'2009',
                             'Unnamed: 54':'2010','Unnamed: 55':'2011','Unnamed: 56':'2012','Unnamed: 57':'2013',
                             'Unnamed: 58':'2014','Unnamed: 59':'2015'})
    gdp['Country']=gdp.index
    gdp.index = pd.RangeIndex(len(gdp.index))
    cols_to_keep =['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    return gdp[cols_to_keep]

def energy():
    xlsx = pd.ExcelFile("Energy+Indicators.xls")
    df = pd.read_excel(xlsx, 'Energy')
    df=df.drop(['Unnamed: 0','Unnamed: 1'], axis=1)
    df = df[16:243]
    df=df.rename(columns ={'Environmental Indicators: Energy': 'Country',
                           'Unnamed: 3':'Energy Supply',
                           'Unnamed: 4':'Energy Supply per Capita',
                           'Unnamed: 5':'% Renewable'})

    df['Country'] = df['Country'].unique()
    df['Country'] = df['Country'].map(lambda x: x.replace('[0-9]',''))
    df['Country'] = df['Country'].map(lambda x: x.split('(')[0])
    df = df.set_index(['Country'])
    df['Energy Supply']=df['Energy Supply']*1000000
    df=df.rename(index={'Republic of Korea':'South Korea',
                        'United States of America':'United States',
                        'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
                        'China, Hong Kong Special Administrative Region3':'Hong Kong'})
    df['Country']=df.index
    df.index = pd.RangeIndex(len(df.index))
    return df

def test_energy(countries):
    """
    Input: a series/ the Country column in Energy
    utf-8 encoded i.e. when reading Energy use
    encoding='utf-8'
    """
    encodedC = '11,7,7,14,7,6,8,19,9,7,5,9,7,10,7,7,10,8,7,7,6,5,7,6,7,32,22,8,6,22,17,8,12,7,10,8,8,6,14,24,4,5,5,9,42,8,7,5,12,10,13,7,4,7,6,14,37,32,7,8,8,18,7,5,11,17,7,7,8,14,16,4,7,6,13,16,5,6,7,7,5,9,6,9,7,10,4,9,8,6,13,6,5,8,7,7,5,9,4,4,7,11,6,5,7,5,6,6,10,5,8,6,10,32,6,7,7,7,5,13,9,10,10,6,8,8,4,5,16,10,10,9,6,10,8,10,10,7,10,7,7,5,5,11,13,11,9,5,7,4,24,6,4,8,5,6,16,8,4,11,6,8,11,5,11,19,7,7,18,6,12,21,11,25,32,5,21,12,7,6,10,12,9,12,8,8,15,7,12,11,5,9,18,5,8,9,6,11,20,10,8,41,11,4,5,19,7,6,12,24,6,6,7,20,14,27,13,28,7,10,7,9,8,25,5,6,8'
    outcome = ['Failed\n', 'Passed\n']



    energy = pd.DataFrame()

    energy['original'] = pd.read_excel('Energy+Indicators.xls',
                                       usecols=[1],encoding='utf-8',
                                       index_col=0).loc[:'Zimbabwe'].index.tolist()
    energy['tested'] = countries.str.len()
    energy['actual'] = encodedC.split(',')
    energy['actual'] = energy['actual'].astype(int)
    try:
        energy['Country'] = countries
    except Exception as e:
        print('Failed, error: ',e)

    res = 'Test number of records: '
    res += outcome[len(countries)==len(energy)]

    res += 'Test the column name: '
    res += outcome [countries.name == 'Country']

    res += 'Equality Test: '
    res += outcome[energy['tested'].equals(energy['actual'])]

    if not energy['tested'].equals(energy['actual']):
        res += '\nMismatched countries:\n'
        mismatch = energy.loc[energy['tested'] != (energy['actual']), [
            'original', 'Country', 'tested', 'actual']].values.tolist()
        res += '\n'.join('"{:}" miss-cleaned as  "{:}"'.format(o, r)
                         for o, r, s, v in mismatch)
    return res
print(test_energy(energy().loc[:,'Country']))



# energy,GDP,ScimEn=energy(),gdp(),scimen()
# print(energy.info())
# print(energy.iloc[[0,-1]])

# print(GDP.info())
# print(GDP.iloc[[0,-1]])


#
# tdf=pd.merge(GDP,energy,how='inner',left_on='Country',right_on='Country')
# tdf=pd.merge(tdf,ScimEn,how='outer',left_on='Country',right_on='Country')
# dataset_size=len(tdf)
# res=tdf.sort_values(by='Rank',ascending=True).head(15)
#
# print(res.iloc[[0,-1]])
# print(dataset_size-15)
# merge_cols_to_keep = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#                       'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
#                       '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
# dataset_set_size= len(merged2)
# merged2=merged2[merge_cols_to_keep].head(15)
#

