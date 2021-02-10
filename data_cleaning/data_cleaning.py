import pandas as pd

df_sac = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\sac_scrapy\redfin_sac.csv')
df_arden = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\sac_scrapy\redfin_arden.csv')
df_citrus = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\sac_scrapy\redfin_citrus.csv')
df_rancho = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\sac_scrapy\redfin_rancho.csv')
df_elk = pd.read_csv(r'C:\Users\ajgal\Documents\GitHub\Sacramento_Housing\sac_scrapy\redfin_elk.csv')

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

# export dataframe in csv format to Github folder
df_total.info()
df_csv_data = df_total.to_csv('redfin_prep.csv')
print('\nCSV String: \n', 'redfin_prep.csv')
