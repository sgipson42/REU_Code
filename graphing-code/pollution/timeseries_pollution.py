#timeseries graph code for specific year
	#do first half then second half of year--make start_date 2019-07-01 for second run
#might need to split filename becuase of filepath included in the string
import sys
import json
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
start_date = str(sys.argv[1]) #2019-01-01 2019-06-30 #2019-07-01 2019-12-31
mid_date = str(sys.argv[2]) #2019-01-01 2019-06-30 #2019-07-01 2019-12-31
start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
mid_date_obj = datetime.datetime.strptime(mid_date, '%Y-%m-%d')
year = start_date_obj.strftime('%Y')
#files = [['no2', 'NO2_2019_forest_5x5_area.json'], ['co', 'CO_2019_forest_5x5_area.json']]
files = [['co', 'CO_2019_forest_5x5_area.json']]
png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/pollution/graphs/'
timeseries_no2 = {}
timeseries_co = {}

for day in range(184):#add all days to dictionary 
    date = start_date_obj + datetime.timedelta(days = day)
    timeseries_no2[date.strftime('%m-%d')] = None
    timeseries_co[date.strftime('%m-%d')] = None

for filename in files: #no2 file, co file
    poln = filename[0]
    print(filename[1])
    with open(filename[1], 'r') as f:
        print(f)
        data = json.load(f)
        for i in data:
            properties = i['properties']
            date = properties["date"]
            file_year = date[:4]
            month = date[5:7]
            day = date[8:10]
            file_date_obj = datetime.datetime.strptime((file_year + '-' + month + '-' + day), '%Y-%m-%d')
            print(file_date_obj)
	    #if file_year == year: #if data is for correct year, save the month_day and concentration info to correct poln dictionary (going through 2019 file only)
            #if file_date_obj <= mid_date_obj: #first half of year
            if file_date_obj >= start_date_obj: #second half of year (middate is now start_date)
                conc = properties[poln] #no2, co
                if poln == 'no2':
                    timeseries_no2[month + '-' + day] = conc
                elif poln == 'co':
                    timeseries_co[month + '-' + day] = conc
            else:
                pass
		
#plot graph
colorblind_palette = sns.color_palette("colorblind")
plt.figure(figsize =(50,10))
#plt.plot(timeseries_no2.keys(), timeseries_no2.values(), marker = 'o', color = colorblind_palette[0], label = 'NO2')
plt.plot(timeseries_co.keys(), timeseries_co.values(), marker = 'o', color = colorblind_palette[1], label = 'CO')
plt.xlabel('Date')
plt.ylabel('CO Concentration (mol/m2)')
plt.xticks(rotation = 45)
plt.title('CO Concentrations Overtime for Ground Truth Area 2019')
plt.grid(True)
plt.legend()
plt.savefig(png_filepath + 'timeseries_CO_5x5_2019_01-06.png')
