#plot a time series of the forest temperature for a year
#change date range on command line, change date list to match size accordingly
import os
import sys
import datetime
import glob
import numpy as np
import seaborn as sns
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

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
    
#def find_closest_coords(f):
#    coords = [1.0566795, 34.7679137] #forest ground truth coords
#    df = pd.read_csv(f)
#    df_bounding_box = df[
#    	(df['latitude'] >= (coords[0]-0.0035)) & #750 height across
#        (df['latitude'] <= (coords[0]+0.0035)) &
#        (df['longitude'] >= (coords[1]-0.0035)) & #750 width across
#        (df['longitude'] <= (coords[1]+0.0035))
#        ]
#    if df_bounding_box.empty:
#        #print('No coordinate data for ',f)
#        pass
#    else: #if coords exists, get the closest point, LST at the point
#        #print('Contains coordinate data for bounding box.')
#        #find coordinate pair closest to ground truth site
#        distances = {} #keys are distances, values are coord pairs
#        for index, row in df_bounding_box.iterrows():
#           lat_comp = row['latitude']
#           lon_comp = row['longitude']
#            distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
#            distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
#        #print('All distances computed.')    
#        coordpair = distances[min(distances)] #this is the closest coordpair
#        if min(distances) < 0.375:
#            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
#            temp = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
#            return temp
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
        #print('Geodataframe for overlapped region:')
        #print(overlap)
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
            #print(distances)
            #print('Number of coordinates for overlapped region:',len(distances))
            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
            LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
            return LST

def main():
    #assign user-defined variables
    #directory = 'East_Africa/'
    directory = '/gypsum/eguide/data/skyler/'
    start_date = str(sys.argv[1]) #20190101 20190701    20190101
    end_date = str(sys.argv[2]) #20190630 20191231  20190331
    start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
    year = start_date_obj.strftime('%Y')
    start_day = start_date_obj.strftime('%Y%j')
    end_day = end_date_obj.strftime('%Y%j')
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    timeseries = {}
    #timeseries_night = {}
    #LST = []
    #dates = []
    
    #for day in range(184):#add all days to dictionary
    #for day in range(90):
    #for day in range(59):
    for day in range(31):
        date = start_date_obj + datetime.timedelta(days = day)
        #).isoformat()
        #dates.append(date.strftime('%m-%d')
        timeseries[date.strftime('%m-%d')] = None
        #timeseries_night[date.strftime('%m-%d')] = None
        #print(timeseries)
    print(timeseries)

    sorted_file_names = sorted(os.listdir(directory))
    #for f in os.listdir(directory): #loop through East Africa directory, all 2018 files
    for f in sorted_file_names: #loop through East Africa directory, all 2018 files
        #print(f)
        if os.path.isfile(directory + f):
            f_date = f[6:18] #2018365.3402
            print(f_date)
            date_obj = datetime.datetime.strptime(f_date, '%Y%j.%H%M')
            #graph_date = date_obj.strftime('%m-%d:%H:%M')
            graph_date = date_obj.strftime('%m-%d')
            #hour = int(date_obj.strftime('%H'))
            if date_obj <= end_date_obj: #with end_date boundary 20180101 20180630
            #if 7<=hour<=20:
            #if date_obj >= start_date_obj: #with start_date boundary 20180701 20181231 
                temp = find_closest_coords('/gypsum/eguide/data/skyler/' + f)
                #print (temp)
    	        #check if LST value returned is nan--if so, don't add it to LST list
                if temp is None:
                    pass
                elif np.isnan(temp):
                    pass
                else:
                    #if 7<=hour<=20: 
                    if 1:
                        print(graph_date)
                        timeseries[graph_date] = int(temp)-273
                        print(timeseries[graph_date])
                #else:
                    #timeseries_night[graph_date] = temp
                #LST.append(temp)
                #dates.append(graph_date)  
                #print(f, 'temp:',temp)
                #print('LSTs:' ,LST)
            else:
            #break
                pass
    print(timeseries)
   #plot graph
    plt.figure(figsize =(15,9))
    #plt.plot(dates, LST, marker = 'o')
    palette = sns.color_palette("colorblind")
    plt.plot(timeseries.keys(), timeseries.values(), marker = 'o', color = palette[2], linewidth=2.5)
    #plt.plot(timeseries.keys(), timeseries.values(), marker = 'o', color = 'brown', label = 'Daytime')
    #plt.plot(timeseries_night.keys(), timeseries_night.values(), marker = 'o', color = 'cadetblue', label = 'Nighttime')
    plt.xlabel('Date', fontsize = 14)
    plt.ylabel('Land Surface Temperature (Celsius)', fontsize = 14)
    plt.xticks(rotation = 45)
    plt.title('LST at Ground Truth Pixel January 2019', fontsize = 16)
    plt.grid(True)
    #plt.legend()
    plt.savefig(png_filepath + 'timeseries_lst_ground_pixel_2019.png')
	
main()
