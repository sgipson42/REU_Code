#!usr/bin/python3
import pandas as pd
import glob
import gzip
from datetime import datetime
#import sys
import argparse
 
def main(start_date, end_date):
    #define country, bounding box, coordinates
    country = 'Uganda' #capitalize
    lat_min = -1.469921875
    lat_max = 4.22021484375
    lon_min = 29.5619140625
    lon_max = 34.9782226563

    #converts string argument to date then int
    start_date_obj = datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.strptime(end_date, '%Y%m%d')
    year = start_date_obj.year
    month = start_date_obj.month
    start_day = start_date_obj.day
    end_day = end_date_obj.day 
	
    #loop through the files in the day range
    for day in range (start_day, end_day+1):
        #get the file for the date specified
        filename = '/home/sgipson_umass_edu/nightfires_data/%d%02d%02d_npp_v30.csv.gz' % (year, month, day)
        with gzip.open(filename) as f:
            df = pd.read_csv(f)
        #df = pd.read_csv(filename)
            #Make a country DataFrame using the bounding box coordinates
            df_country = df[
            (df['Lat_GMTCO'] >= lat_min) &
            (df['Lat_GMTCO'] <= lat_max) &
            (df['Lon_GMTCO'] >= lon_min) &
            (df['Lon_GMTCO'] <= lon_max)
            ]
            #save the data as a csv to the correct filepath (name included)
            #savefile = filename.split('/')[-1] #saves with .gz
            savefile = '%d%02d%02d_npp_v30.csv' % (year, month, day) #saves with .csv
            store_path = f"/work/pi_jtaneja_umass_edu/sgipson/nightfires_data/East_Africa/{country}/{savefile}"
            df_country.to_csv(store_path, index = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File and Model Parameters')
    parser.add_argument('--start_date', type = str, required = True)
    parser.add_argument('--end_date', type = str, required = True)
    args = parser.parse_args()
    start_date = args.start_date
    end_date = args.end_date

    main(start_date, end_date)
