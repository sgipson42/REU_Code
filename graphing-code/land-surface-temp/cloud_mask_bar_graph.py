#!usr/bin/python3
#cloud masking value distribution at 6 month intervals
import pandas as pd
import json

country = 'Kenya' #Rwanda
all_files = ['/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20180101_npp_v30.csv' % (country), 
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20180601_npp_v30.csv' % (country), 
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20190101_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20190601_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20200101_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20200601_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20210101_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20210601_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20220101_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20220601_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20230101_npp_v30.csv' % (country),
	'/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/%s/20230601_npp_v30.csv' % (country)
]

df_cloud = pd.DataFrame(columns = ['Date', '0', '1', '2', '3', '999999'])
 
#loop through the files
for file in all_files:
    df = pd.read_csv(file)
    filename = file.split('/')[-1] #saves with .csv
    date = filename[5:6] + '/1/' + filename[2:4]
	
    #add variables to dataframe
    df_row = json.loads(df['Cloud_Mask'].value_counts().to_json())
    df_row['Date'] = date
    df_cloud = pd.concat([df_cloud, pd.DataFrame([df_row])], ignore_index = True)

#plot graph
ax = df_cloud.plot(x = "Date", y = ["0", "1", "2", "3", "999999"], kind = "bar", title = "Distribution of Cloud Mask Values", rot = 70)
fig = ax.get_figure()
fig.savefig('/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/Cloud_Mask_Bar.png')
