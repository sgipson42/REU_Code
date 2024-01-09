#diurnal zscores

import sys
import math
import os
import datetime
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import radians, cos, sin, asin, sqrt

def calculate_z_scores(mean, data):
    std_dev = np.std(data)
    z_scores = (data - mean) / std_dev
    return z_scores

#0.001∘=111 meters
#do +/-0.007 change to get 770 meters in any direction
def haversine(lon1, lat1, lon2, lat2):
#Calculate the great circle distance in kilometers between two points on the earth (specified in decimal degrees)
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
    
def find_closest_coords(f):
    coords = [1.0566795, 34.7679137] #forest ground truth coords
    df = pd.read_csv(f)
    df_bounding_box = df[
        (df['latitude'] >= (coords[0]-0.0035)) &
        (df['latitude'] <= (coords[0]+0.0035)) &
        (df['longitude'] >= (coords[1]-0.0035)) &
        (df['longitude'] <= (coords[1]+0.0035))
        ]
    if df_bounding_box.empty:
        #print('No coordinate data for ',f)
        pass
    else: #if coords exists, get the closest point, LST at the point
        #print('Contains coordinate data for bounding box.')
        #find coordinate pair closest to ground truth site
        distances = {} #keys are distances, values are coord pairs
        for index, row in df_bounding_box.iterrows():
            lat_comp = row['latitude']
            lon_comp = row['longitude']
            distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
            distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
        #print('All distances computed.')    
        coordpair = distances[min(distances)] #this is the closest coordpair
        if min(distances) < 0.375:
            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
            LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
            return LST
        
def main():
    #assign user-defined variables
    directory = 'East_Africa/'
    #start_date = str(sys.argv[1]) #20180101
    #end_date = str(sys.argv[2]) #201801231
    #mid_date = str(sys.argv[2]) #20180630
    #start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    #end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
    #mid_date_obj = datetime.datetime.strptime(mid_date, '%Y%m%d') #the date you want to stop averaging at, and compare zscore after 
    #year = start_date_obj.strftime('%Y')
    #start_day = start_date_obj.strftime('%Y%j')
    #end_day = end_date_obj.strftime('%Y%j')
    #mid_day = mid_date_obj.strftime('%Y%j')
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    LST = []
    hours = []
    

    for f in os.listdir(directory): #loop through East Africa directory, all 2018 files
        date = f[6:18] #2018365.3402
        temp = find_closest_coords('East_Africa/' + f)
        print(temp)
    	#check if LST value returned is nan--if so, don't add it to calculation list
        if temp is None:
            #print('LST value is None for this point.')
            pass
        elif np.isnan(temp):
            pass
            #print('LST value is absent for this point.')
            #check which list to add the value to based on time of year
        else:
            date_obj = datetime.datetime.strptime(date, '%Y%j.%H%M')
            hour = int(date_obj.strftime('%H'))
            hours.append(hour)
            LST.append(temp)

    # Create the box and whiskers plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(LST, positions=hours, widths=0.6, patch_artist=True)

    # Customize the plot
    plt.xlabel('Hour of the Day')
    plt.ylabel('Land Surface Temperature')
    plt.title('Box and Whiskers Plot of Land Surface Temperature vs. Hour of the Day 2018')
    plt.xticks(range(24), range(24))  # Assuming hours range from 0 to 23
    plt.grid(True)

    # Show the plot
    plt.show()
    plt.savefig(png_filepath + 'box_plot_lst_hours_forest_pixel_%d.png' % (int(year)))
    #plt.savefig(png_filepath + 'box_plot_lst_hours_forest_%d.png' % (int(year)))
   
	
main()

