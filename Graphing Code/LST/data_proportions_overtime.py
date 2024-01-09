#find the proportion of usable LST data for all of East Africa across some time span
#do the same for the specific forest region
import pandas as pd
import sys
import datetime
import glob
import matplotlib.pyplot as plt
#adjust dates as needed
	#currently loops through every day in the year
	#could do by week instead
		#make a mini loop for seven times, advance it daily and outer loop weekly
		#make sure that never passes end_date
		

#assign user-defined variables
#directory = '/work/pi_jtaneja_umass_edu/sgipson/LST/East_Africa/VNP21.'
directory = 'East_Africa/VNP21.'
start_date = str(sys.argv[1]) #20180101
end_date = str(sys.argv[2]) #20181231
start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
year = start_date_obj.strftime('%Y')
curr_week = start_date_obj
png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
df = pd.DataFrame(columns = ['Date', 'Percentage of Absent Data', 'Percentage of Usable Data'])

#loop through the days
while curr_week <= end_date_obj:
    weekly_files = []
    curr_day = curr_week
    #get all the files for the week
    for day in range (1,7):
        year_day = curr_day.strftime('%Y%j')
        files = glob.glob(directory + year_day + '.*.csv')
        weekly_files.append(files) #add list of daily files to list of weekly files
        curr_day += datetime.timedelta(days=1)
    #assign date and initialize loop variables    
    month = curr_week.strftime('%m')
    day = curr_week.strftime('%d')
    date = month + '-' + day
    temp_count = 0
    fill_count = 0
    total_len = 0
    #loop though the files for this week
    print(weekly_files)
    for day_files in weekly_files:#loop thourgh daily files
        for f in files: #loop through files per day
            #add the # of usable temps and fill values to the temp_count and fill_count for the week
            #add the number of rows to the total count
            df_file = pd.read_csv(f)
            LST = df_file['LST'] #column of temp values for multiple coords in a day
            temp_count += LST.count() #num of not null values
            fill_count += len(LST) - LST.count() #num of null values
            total_len += len(LST)

    #after updating temps, fills, and length, to include the file's values, update the total percentages for this WEEK   
    #only if there are any values available (meaning files is not empty)
    if total_len != 0: 
        temp_percent = (temp_count/total_len) *100 
        fill_percent = (fill_count/total_len) *100
    
        #add variables to the dataframe (only for days where there is any LST info available)
        df_row = {'Date' : date, 'Percentage of Absent Data' : fill_percent, 'Percentage of Usable Data' : temp_percent}
        df = pd.concat([df, pd.DataFrame([df_row])], ignore_index = True)
	
    #advance loop to next week
    curr_week += datetime.timedelta(days=7)

#plot graph
ax = df.plot(x = 'Date', y = ['Percentage of Absent Data', 'Percentage of Usable Data'], kind = "bar", title = "Proportion of Usable Data for LST in East Africa by Week", rot = 45)
fig = ax.get_figure()
fig.set_figwidth(15)
fig.savefig('/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/%d_LST_weekly_proportions_EastAfrica.png' % (int(year)))
