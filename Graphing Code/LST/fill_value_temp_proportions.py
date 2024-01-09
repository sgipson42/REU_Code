#to create graph of proportion of pixels with a fill value or temperature reading per line number

#loop over every pixel in each line--row is line num, column is pixel num--temp value displayed per pixel
#add each new column (by pixel num) to a dataframe
#make each column a series, get temp value counts and fill counts and graph PROPORTION of each

import netCDF4 as nc
import pandas as pd
import matplotlib

#netcdf_file = '/Users/skyler/Downloads/VNP21.A2019065.2336.001.2019121164902.nc'
netcdf_file = '/home/sgipson_umass_edu/VNP21.A2019065.2336.001.2019121164902.nc'
ds_nc = nc.Dataset(netcdf_file)
LST = ds_nc['VIIRS_Swath_LSTE/Data Fields'].variables['LST']
df = pd.DataFrame(columns = ['Line Number', 'Fill Value Count', 'Temperature Reading Count'])
temp_percent_sum = 0

#which way does series need to go?
for line_num in range(0, 3248): #3248 rows, 3200 columns
        LST_series = pd.Series(LST[line_num, :])
        #temp_count = LST_series.notnull().sum()
        #fill_count = LST_series.size - temp_count
        temp_percent = (LST_series.notnull().sum()/LST_series.size) *100
        fill_percent = ((LST_series.size - (LST_series.notnull().sum()))/LST_series.size) *100
        temp_percent_sum += temp_percent

        df_row = {'Line Number' : line_num, 'Fill Value Percentage' : fill_percent, 'Temperature Reading Percentage' : temp_percent}
        df = pd.concat([df, pd.DataFrame([df_row])])

#plot graph
ave_temp_percent =  temp_percent_sum/3248
print(ave_temp_percent) 
#16.718663408251256--by pixel num
#16.71866340825123--by line num
ax = df.plot(x = "Line Number", y = ["Fill Value Percentage", "Temperature Reading Percentage"], kind = "bar", title = "Proportion of Fill Values to Temperature Readings", rot = 45, figsize=(35,15))
fig = ax.get_figure()
#fig.savefig('/Users/skyler/Desktop/LST_fill_proportions_by_line_num.png')
fig.savefig('/home/sgipson_umass_edu/LST_fill_proportions_by_line_num.png')
