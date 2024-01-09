#diurnal zscores
#lst on y axis
#hours on x axis
#make a list for each hour data is collected
#each hour will have temperatures in it
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
    p1=Point(34.7679137, 1.0566795)
    gdf=gpd.GeoSeries(p1)
    gdf.set_crs('EPSG:4326', inplace = True)
    gdf2 =gdf.to_crs('EPSG:32733')
    gdf3 = gdf2.buffer(375, cap_style=3)#bounding box is the exact size you need
    gdf4 = gdf3.to_crs('EPSG:4326')
    gdf_box = gpd.GeoDataFrame(geometry=gdf4)
    df = pd.read_csv(f)
    gdf_granule = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326'))
    overlap = gdf_box.overlay(gdf_granule, how='intersection', keep_geom_type=False)
    if overlap.empty:
        pass
    else: #if coords exists, get the closest point, LST at the point
        print('Geodataframe for overlapped region:')
        print(overlap)
        #find coordinate pair closest to ground truth site
        distances = {} #keys are distances, values are coord pairs
        for index, row in overlap.iterrows():
            lat_comp = row['latitude']
            lon_comp = row['longitude']
            distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
            distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
        #print('All distances computed.')
        coordpair = distances[min(distances)] #this is the closest coordpair
        #print(overlap)
        #print(distances[min(distances)])
        if distances:
            print(distances)
            print('Number of coordinates for overlapped region:',len(distances))
            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
            LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
            return LST
    
def main():
    #assign user-defined variables
    directory = 'East_Africa/'
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    hours = {'Daytime':[], 'Nighttime':[]}

    for f in os.listdir(directory): #loop through East Africa directory, all 2018 files
        date = f[6:18] #2018365.3402
        temp = find_closest_coords('East_Africa/' + f)
        #print(temp)
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
            print(date)
            hour = int(date_obj.strftime('%H'))
            if hour==10 or hour==11:
                hours['Daytime'].append(temp)
            else:#hour is 22 or 23
                hours['Nighttime'].append(temp)
                

    print(hours)   
    fig, ax = plt.subplots()
    ax.boxplot(hours.values(), widths = (0.5, 0.5))
    ax.set_xticklabels(hours.keys())
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Land Surface Temperature (K)')
    #ax.set_title('Diurnal Land Surface Temperature for Forest 2018')
    ax.set_title('2019 Diurnal LST at Ground Truth Site')
    ax.grid(True)
    #plt.savefig('/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/box_plot_lst_hours_forest_pixel_2018.png')
    #plt.savefig(png_filepath + 'box_plot_lst_diurnal_forest_2018.png')
    plt.savefig(png_filepath + 'box_plot_lst_diurnal_forest_pixel_2019.png')


   # Create the box and whiskers plot
    #fig, ax = plt.subplots()
    # Plot box plots for each key-value pair
    #for key, values in hours.items():
     #   ax.boxplot(values, positions=[key], patch_artist=True)
    # Customize the plot
    #ax.set_xlabel('Hour of Day')
    #ax.set_ylabel('Land Surface Temperature')
    #ax.set_title('Diurnal Land Surface Temperature for Ground Truth Site 2018')
    #ax.set_xticks(range(1, len(hours) + 1))
    #ax.set_xticklabels(hours.keys())
    #ax.grid(True)
    #plt.savefig(png_filepath + 'box_plot_lst_diurnal_forest_pixel_2018.png')
    #plt.savefig(png_filepath + 'box_plot_lst_diurnal_forest_2018.png')
   
	
main()

