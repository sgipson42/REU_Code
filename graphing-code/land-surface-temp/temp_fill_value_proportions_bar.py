#!usr/bin/python3
import pandas as pd
import matplotlib

country = 'Kenya'
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

df_temp = pd.DataFrame(columns = ['Date', 'Fill Value Percentage', 'Temperature Reading Percentage'])
 
for file in all_files:
    df = pd.read_csv(file)
    filename = file.split('/')[-1] #saves with .csv
    date = filename[5:6] + '/1/' + filename[2:4]
    
    #get temp columns as series, number of fill values, and number of temp values
    ser = df.loc[:, 'Temp_Bkg'] #Temp_BB #Temp_Bkg
    fill_count = ser.value_counts().get(999999, 0)
    temp_count = ser.size - fill_count
    fill_percent = fill_count/ser.size
    temp_percent = temp_count/ser.size

    #add variables to the dataframe
    df_row = {'Date' : date, 'Fill Value Percentage' : fill_percent, 'Temperature Reading Percentage' : temp_percent}
    df_temp = pd.concat([df_temp, pd.DataFrame([df_row])], ignore_index = True)

#plot graph
ax = df_temp.plot(x = "Date", y = ["Fill Value Percentage", "Temperature Reading Percentage"], kind = "bar", title = "Proportion of Fill Values to Earth Temperature Values Read", rot = 45)
fig = ax.get_figure()
fig.savefig('/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/Temp_Bkg_Bar_Proportions.png')
