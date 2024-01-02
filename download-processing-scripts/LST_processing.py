import pandas as pd
import xarray as xr
import glob
from pathlib import Path
import sys
import os

# coordinates for region of interest
lat_min = -4.6923828125 
lat_max = 5.49228515625 
lon_min = 28.8576171875 
lon_max = 41.883984375

 
year = str(sys.argv[1]) #date='2019'
directory_path = '/gypsum/eguide/data/skyler/raw_data/%d/' % (int(year))
filepath= '/gypsum/eguide/data/skyler/'
filecount = 0
#loop through the list of files in the year directory
for f in os.listdir(directory_path):
    print(directory_path)
    print(f)
    filename = f.split('/')[-1]  #VNP21.2018365.1112.nc
    print(filename)
    f_checksize = Path(directory_path+f)
    print(f_checksize)
    if (f_checksize.stat().st_size > 1000):
        csv_filepath = filepath + filename[:18] + '.csv'
        #convert the geolocation fields to a dataframe, filter by East Africa range
        #create geolocation dataframe
        ds = xr.open_dataset(directory_path + f, group =  'VIIRS_Swath_LSTE/Geolocation Fields')
        df = ds.to_dataframe()
	
        #filter coordinates
        df_bounding_box = df[
            (df['latitude'] >= lat_min) &
            (df['latitude'] <= lat_max) &
            (df['longitude'] >= lon_min) &
            (df['longitude'] <= lon_max)
            ]
    		
        #check that the dataframe has coordinates before saving to csv
        if (df_bounding_box.empty):
            print ('Bounding box for ' + filename + ' has no data.')
        else:
            filecount += 1
            ds_data = xr.open_dataset(directory_path + f, group =  'VIIRS_Swath_LSTE/Data Fields')
            df_data_full = ds_data.to_dataframe()
            df_data = pd.DataFrame(df_data_full, columns = ['LST', 'LST_err'])
            df = df_bounding_box.join(df_data)
            #convert dataframe to CSV
            df.to_csv(csv_filepath)
    else:
        print('File size of',filename, 'is:', f_checksize.stat().st_size)
print(filecount)
