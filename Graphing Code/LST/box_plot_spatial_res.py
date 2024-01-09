#get the z-score list for a bunch of pixels at one resolution, use 2018/2019 
#loop through the files, loop through coordinate list, loop through the spatial resolutions

#add all of the LST values in that resolution box to the cdf? or average all of them and then add the avergaed value? 
#check that overlay method does what you think it does
#add in coordinate list
#change y-axis color to black
#2018 and 2019, or just 2019?
import sys
import math
import os
import datetime
import glob
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import radians, cos, sin, asin, sqrt

def calculate_z_scores(mean, data):
    std_dev = np.std(data)
    z_scores = (data - mean) / std_dev
    return z_scores

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

def find_closest_coords(f, coordinates, half_res):
    #coords = [1.0566795, 34.7679137] #forest ground truth coords
    #p1=Point(34.7679137, 1.0566795)
    p1 = Point(coordinates[1], coordinates[0])
    gdf=gpd.GeoSeries(p1)
    gdf.set_crs('EPSG:4326', inplace = True)
    gdf2 =gdf.to_crs('EPSG:32733')
    gdf3 = gdf2.buffer(half_res, cap_style=3)#bounding box is the exact size you need
    gdf4 = gdf3.to_crs('EPSG:4326')
    gdf_box = gpd.GeoDataFrame(geometry=gdf4)
    df = pd.read_csv(f)
    gdf_granule = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326'))
    overlap = gdf_box.overlay(gdf_granule, how='intersection', keep_geom_type=False)
    if overlap.empty:
        pass
    else: #add all LST values for the overlapped region (the correct spatial res) to a list, return the list
        print('Geodataframe for overlapped region:')
        print(overlap)
        #find coordinate pair closest to ground truth site ONLY IF the half_res is 375 (at one pixel, other you want more readings
        LST_list = []
        if half_res == 375:
            distances = {} #keys are distances, values are coord pairs
            for index, row in overlap.iterrows():
                lat_comp = row['latitude']
                lon_comp = row['longitude']
                distance = haversine(coordinates[1], coordinates[0], lon_comp, lat_comp)
                distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
            #print('All distances computed.')
            coordpair = distances[min(distances)] #this is the closest coordpair
            #print(overlap)
            #print(distances[min(distances)])
            if distances:
                #print(distances)
                #print('Number of coordinates for overlapped region:',len(distances))
                row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
                LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
                LST_list.append(LST)

        else: #if at higher resolution, want multiple LST readings
            for index, row in overlap.iterrows():
                LST_list.append(row['LST'])

        return LST_list
    
def main():
    #assign user-defined variables
    first_directory = 'East_Africa/'
    second_directory = '/gypsum/eguide/data/skyler/'
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    #coords = [[-1.287214, 36.823147], [-1.290214, 36.833147],[-1.290214, 36.79147],[-1.298214, 36.80147],[-1.298214, 36.85147],[-1.260214, 36.82147],[-1.280214, 36.790147],[-1.270214, 36.829147],[-1.287214, 36.850147],[-1.307214, 36.823147]]
    coords = [[-1.287214, 36.823147], [-1.290214, 36.833147],[-1.290214, 36.79147],[-1.298214, 36.80147],[-1.298214, 36.85147],[-1.260214, 36.82147],[-1.280214, 36.790147],[-1.270214, 36.829147],[-1.287214, 36.850147],[-1.307214, 36.823147], [1.0566795, 34.7679137],[1.0566795, 34.7479137],[1.0606795, 34.7479137],[1.0606795, 34.7699137],[1.0576795, 34.7759137],[1.0536795, 34.7359137],[1.0436795, 34.7659137],[1.0336795, 34.7729137],[1.0590795, 34.7529137], [1.0590795, 34.7729137],[0.032167, 37.745747], [0.032167, 37.725747],[0.035167, 37.736747],[0.035167, 37.745747],[0.030167, 37.760747],[0.025167, 37.749747],[0.036167, 37.745747],[0.034167, 37.742747],[0.031167, 37.744747],[0.029167, 37.749747],[1.011106, 37.736814],[1.011106, 37.716814],[1.011106, 37.756814],[1.031106, 37.736814],[1.000106, 37.736814],[1.008106, 37.734814],[1.015106, 37.734814],[1.015106, 37.739814],[1.014706, 37.756814],[1.010706, 37.750014]]

    first_grids = {'1x1 (750m)':[], '3x3 (2250m)':[], '5x5 (3750m)':[]}
    second_grids = {'1x1 (750m)':[], '3x3 (2250m)':[], '5x5 (3750m)':[]}
    half_res = [375, 1125, 1875] #750, 750*3, 750*5

    for f in os.listdir(first_directory): #loop through East Africa directory, all 2018 files
        if os.path.isfile(first_directory + f):
            day = f[10:13]
            hour = f[14:16]
            if (int(day) < 182) and (7<=int(hour)<=19): #first half of year and in the DAYTIME
            #if int(day) < 10: #first half of year
                for coord in coords:
                    key_count = 0
                    for key in first_grids.keys():
                        date = f[6:18] #2018365.3402
                        temps = find_closest_coords(first_directory + f, coord, half_res[key_count])
                        #print(temps)
                        if temps:
                            print(date)
                            key_count += 1
                            for temp in temps:
                                if temp is None:
                                    pass
                                elif np.isnan(temp):
                                    pass
                                else: #if temp is readable
                                    first_grids[key].append(temp)
            else:
                pass
                
    sorted_file_names = sorted(os.listdir(second_directory))
    for f in sorted_file_names: #loop through 2019 East Africa directory, all 2019 files
    #for f in os.listdir(second_directory): #loop through East Africa directory, all 2018 files
        if os.path.isfile(second_directory + f):
            day = f[10:13]
            hour = f[14:16]
            if (int(day) < 182) and (7<=int(hour)<=19): #first half of year and in the DAYTIME
            #if int(day) < 10:
                for coord in coords:
                    key_count = 0
                    for key in second_grids.keys():
                        date = f[6:18] #2018365.3402
                        temps = find_closest_coords(second_directory + f, coord, half_res[key_count])
                        if temps:
                            print(date)
                            key_count += 1
                            for temp in temps:
                                if temp is None:
                                    pass
                                elif np.isnan(temp):
                                    pass
                                else: #if temp is readable
                                    second_grids[key].append(temp)
            else:
                pass
    
    #after looping through all days to get dict of resolutions at various locations
    palette = sns.color_palette("colorblind")
    #color_positions = [[0, palette[0]], [1, palette[2]], [2, palette[9]]
    key_count = 0
    fig, ax = plt.subplots()
    for key in first_grids.keys(): #for each resolution, make the z-score list
        first_list = first_grids[key]
        second_list = second_grids[key]
        #get mean from first year, and compute zscores for year against it
        z_scores = calculate_z_scores(np.mean(first_list), second_list)

        print('First:',first_grids[key])
        print('Second:',second_grids[key])
        c = palette[key_count]
        ax.boxplot(z_scores, positions=[key_count], widths=0.6, notch = True, patch_artist = True, boxprops=dict(facecolor=c, color=c), capprops=dict(color=c), whiskerprops=dict(color=c), flierprops=dict(color=c, markeredgecolor=c),medianprops=dict(color=c))
        key_count += 1
        
    #after all keys loop through
    ax.set_xticklabels(first_grids.keys())
    ax.set_xlabel('Pixel Grid Size and Resolution (Meters)')
    ax.set_ylabel('Z-Scores of LST')
    ax.set_title('Distribution of Daytime LST Z-Scores by Spatial Resolution 2018-2019')
    ax.grid(True)
    plt.savefig(png_filepath + 'box_plot_spatial_res_2018_2019.png')

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

