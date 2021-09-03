import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_sac = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\data\sac_scrapy\redfin_sac.csv')
df_arden = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\data\sac_scrapy\redfin_arden.csv')
df_citrus = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\data\sac_scrapy\redfin_citrus.csv')
df_rancho = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\data\sac_scrapy\redfin_rancho.csv')
df_elk = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\data\sac_scrapy\redfin_elk.csv')

# combine all data collected into a single dataframe
df_total = pd.concat([df_sac, df_arden, df_citrus, df_rancho, df_elk], ignore_index=True)
df_total = df_total.reset_index(drop=True)

# convert bath strings into float values and change blanks into zeroes
df_total['baths'] = df_total['baths'].apply(lambda x: (x.split(' Bath')[0]))
df_total['baths'] = df_total['baths'].replace(to_replace='Baths', value=0)
df_total['baths'] = df_total['baths'].apply(lambda x: float(x))

# convert bed strings into float values and change blanks into zeroes
df_total['beds'] = df_total['beds'].apply(lambda x: (x.split(' Bed')[0]))
df_total['beds'] = df_total['beds'].replace(to_replace='Beds', value=0)
df_total['beds'] = df_total['beds'].apply(lambda x: float(x))

# convert pricing to float values using regex
df_total['price'] = df_total['price'].replace('[$,+]', '', regex=True).astype(int)

# remove units from Sq. Ft column and delete homes where Sq.Ft is none
df_total['sq_ft'] = df_total['sq_ft'].apply(lambda x: (x.split(' Sq. Ft.')[0]))
df_total = df_total[df_total.sq_ft != 'Sq. Ft.']
df_total['sq_ft'] = df_total['sq_ft'].replace('[,]', '', regex=True).astype(int)

# add zip code column from address column
df_total['zip_code'] = df_total['address'].apply(lambda x: x[-5:])
df_total['zip_code'][216] = '95864'
df_total['zip_code'][384] = '95864'
df_total['zip_code'][159] = '95823'

df_total['zip_code'].nunique()

# add city column
df_total['city'] = df_total['address'].apply(lambda x: (x.split(', ')[1].title()))

# add street column
df_total['street'] = df_total['address'].apply(lambda x: (x.split(', ')[0].title()))

# fill null values for brokerage with 'None'
df_total.info()
df_total['brokerage'] = df_total['brokerage'].fillna('None')
df_total.info()

# histogram plot for price
sns.histplot(df_total['price'], bins=20)
plt.show()

# remove outliers
upper_limit = df_total['price'].quantile(0.95)
lower_limit = df_total['price'].quantile(0.05)
df_edit = df_total[(df_total['price'] > lower_limit) & (df_total['price'] < upper_limit)]

# histogram plot after removing outliers
sns.histplot(df_edit['price'], bins=20)
plt.show()

# remove lines without beds or baths
index_zero_beds = df_edit[df_edit['beds'] < 1 ].index
df_edit.drop(index_zero_beds,inplace=True)

index_zero_baths = df_edit[df_edit['baths'] < 1 ].index
df_edit.drop(index_zero_baths,inplace=True)

# export file to csv without index
df_final = df_edit
df_final.info()

df_final.to_csv('redfin_prep.csv',index=False)
