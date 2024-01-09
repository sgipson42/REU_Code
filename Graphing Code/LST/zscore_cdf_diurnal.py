#diurnal zscores at one pixel, one location, 750 m
import seaborn as sns
import sys
import math
import os
import geopandas as gpd
import shapely
from shapely.geometry import Point
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
    #gdf3 = gdf2.buffer(1125)#radius--not as many valid results back, as with square
    #gdf3 = gdf2.buffer(1590.33009)#hypotenuse radius--more results, but still sometimes a few
    gdf3 = gdf2.buffer(375, cap_style=3)#bounding box is the exact size you need
    gdf4 = gdf3.to_crs('EPSG:4326')
    gdf_box = gpd.GeoDataFrame(geometry=gdf4)
    df = pd.read_csv(f)
    gdf_granule = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326'))
    overlap = gdf_box.overlay(gdf_granule, how='intersection', keep_geom_type=False)
    if overlap.empty:
        #print('No coordinate data for ',f)
        pass
    else: #if coords exists, get the closest point, LST at the point
        #print('Geodataframe for overlapped region:')
        #print(overlap)
        #print('Contains coordinate data for bounding box.')
        #find coordinate pair closest to ground truth site
        distances = {} #keys are distances, values are coord pairs
        #for index, row in df_bounding_box.iterrows():
        for index, row in overlap.iterrows():
            lat_comp = row['latitude']
            lon_comp = row['longitude']
            distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
            #if distance < 1.125:
            distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
        #print('All distances computed.')    
        coordpair = distances[min(distances)] #this is the closest coordpair
        #print(overlap)
        #print(distances[min(distances)])
        #if min(distances) < 0.375:
        if distances:
            #print(distances)
            #print('Number of coordinates for overlapped region:',len(distances))
        #if min(distances) <= 1.125:
            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
            LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
            return LST    
#def find_closest_coords(f):
    #coords = [1.0566795, 34.7679137] #forest ground truth coords
    #coords = [1.011106, 37.736814] #savanna coords
    #coords = [0.032167, 37.745747] #agricultural coords
#    coords = [1.287214, 36.823147] #nairobi coords
#    df = pd.read_csv(f)
#    df_bounding_box = df[
#        (df['latitude'] >= (coords[0]-0.0035)) &
#        (df['latitude'] <= (coords[0]+0.0035)) &
#        (df['longitude'] >= (coords[1]-0.0035)) &
#        (df['longitude'] <= (coords[1]+0.0035))
#        ]
#    if df_bounding_box.empty:
        #print('No coordinate data for ',f)
#        pass
#    else: #if coords exists, get the closest point, LST at the point
        #print('Contains coordinate data for bounding box.')
        #find coordinate pair closest to ground truth site
#        distances = {} #keys are distances, values are coord pairs
#        for index, row in df_bounding_box.iterrows():
#            lat_comp = row['latitude']
#            lon_comp = row['longitude']
#            distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
#            distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
        #print('All distances computed.')    
#        coordpair = distances[min(distances)] #this is the closest coordpair
#        if min(distances) < 0.375:
#            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
#            LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
#            return LST
        
def main():
    #assign user-defined variables
    first_directory = 'East_Africa/'
    second_directory = '/gypsum/eguide/data/skyler/'
    #start_date = str(sys.argv[1]) #20180101
    #end_date = str(sys.argv[2]) #201801231
    #mid_date = str(sys.argv[2]) #20180
    #start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    #end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
    #mid_date_obj = datetime.datetime.strptime(mid_date, '%Y%m%d') #the date you want to stop averaging at, and compare zscore after 
    #year = start_date_obj.strftime('%Y')
    #start_day = start_date_obj.strftime('%Y%j')
    #end_day = end_date_obj.strftime('%Y%j')
    #mid_day = mid_date_obj.strftime('%Y%j')
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    daytime_first_LST = []
    daytime_second_LST = []
    nighttime_first_LST = []
    nighttime_second_LST = []
    #results = pd.DataFrame(columns = ['daytime_first', 'daytime_second', 'daytime_zscores', 'nighttime_first', 'nighttime_second', 'nighttime_zsc
    #timeseries = {}
    #timeseries_night = {}
    #coords = [1.0566795, 34.7679137]
    #for the zscore, dont need to add dates at all-just get a list daytime LST measurements for first half of year, nightime for first half, and same for second half
    
    #loop through 2018 directory and add to the FIRST LST lists
    for f in os.listdir(first_directory): #loop through East Africa directory, all 2018 files
        date = f[6:18] #2018365.3402
        day = f[10:13] #2018365.3402
        if int(day)<182:
            LST = find_closest_coords('East_Africa/' + f)
            print(date)
        #print(LST)
    	#check if LST value returned is nan--if so, don't add it to calculation list
            if LST is None:
            #print('LST value is None for this point.')
                pass
            elif np.isnan(LST):
                pass
            #print('LST value is absent for this point.')
            #check which list to add the value to based on time of year
            else:
                date_obj = datetime.datetime.strptime(date, '%Y%j.%H%M')
            #curr_day = datetime.datetime.strptime(date[:7], '%Y%j')
                hour = int(date_obj.strftime('%H'))
            #hour = int(datetime.datetime.strptime('%H'))
            #print(curr_day, hour)
            #if curr_day <= mid_date_obj: #in first half of year
                if 7<=hour<=19: #daytime measurement
                    daytime_first_LST.append(LST)
                else:
                    nighttime_first_LST.append(LST)

    sorted_file_names = sorted(os.listdir(second_directory))
    for f in sorted_file_names:
    #for f in os.listdir(second_directory): #loop through 2019 East Africa directory, all 2019 files
        #print(f)
        if os.path.isfile(second_directory + f):
            date = f[6:18] #2018365.3402
            day = f[10:13]
            if int(day)<182:
                LST = find_closest_coords(second_directory + f)
                print(date)
                if LST is None:
                    pass
                elif np.isnan(LST):
                    pass
                else:
                    date_obj = datetime.datetime.strptime(date, '%Y%j.%H%M')
                    hour = int(date_obj.strftime('%H'))
                    if 7<=hour<=19: #daytime measurement
                        daytime_second_LST.append(LST)
                    else:
                        nighttime_second_LST.append(LST)
    
    #once the full list of LST values is gotten for first and second halves
    #get mean from first year, and compute zscores for second half of year against it
    daytime_z_scores = calculate_z_scores(np.mean(daytime_first_LST), daytime_second_LST) 
    nighttime_z_scores = calculate_z_scores(np.mean(nighttime_first_LST), nighttime_second_LST) 

    #print useful information
    print('Mean of daytime first:' ,np.mean(daytime_first_LST))
    print('Daytime First:',daytime_first_LST)
    print('Daytime Second:',daytime_second_LST)
    print('z-scores from daytime second:' ,daytime_z_scores)
    
    print('Mean of nighttime first:' ,np.mean(nighttime_first_LST))
    print('Nighttime First:',nighttime_first_LST)
    print('Nighttime Second:',nighttime_second_LST)
    print('z-scores from nighttime second:' ,nighttime_z_scores)

    #plot daytime z-scores
    palette = sns.color_palette("colorblind")
    count, bins_count = np.histogram(daytime_z_scores, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label = 'Daytime', color = palette[3])
    #plot nighttime zscores
    count, bins_count = np.histogram(nighttime_z_scores, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label = 'Nighttime', color = palette[9])
    #pdf_values = norm.pdf(z_scores)
    #cdf_values = np.cumsum(pdf_values)
    #cdf_values /= cdf_values[-1]  # Normalize the CDF to have a maximum value of 1
    #plt.rcParams["figure.figsize"] = [7.50, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    #plt.plot(z_scores, cdf_values, marker='o')
    plt.xlabel('LST Z-Scores', fontsize = 16)
    plt.ylabel('Probabilities', fontsize = 16)
    plt.title('CDF of Diurnal LST Z-Scores at Forest Pixel 2018/2019', fontsize = 18)
    plt.grid(True)
    plt.legend()
    #plt.show()
    plt.savefig(png_filepath + 'diurnal_zscore_lst_cdf_forest_pixel_%d.png' % (int(year)))
    #plt.savefig(png_filepath + 'diurnal_zscore_lst_cdf_nairobi_pixel_%d.png' % (int(year)))
	
main()
