#z-score CDF for 3x3 grid--one daytime, and one nighttime as separate graphs
import sys
import math
import os
import datetime
import glob
import geopandas as gpd
import shapely
from shapely.geometry import Point
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
    #gdf3 = gdf2.buffer(1590.99026)#radius--not as many valid results back, as with square and check that <distance later method
    gdf3 = gdf2.buffer(1125, cap_style=3)#square where 1125 is half the length
    gdf4 = gdf3.to_crs('EPSG:4326')
    #print(gdf4.total_bounds)
    gdf_box = gpd.GeoDataFrame(geometry=gdf4) #2250m box with point as center
    #print(p1)
    #print(gdf4.bounds)
    #bounds = pd.Series(gdf4.bounds.iloc[0])
    df = pd.read_csv(f)
    gdf_granule = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326')) #East Africa bounding box from file
    overlap = gdf_box.overlay(gdf_granule, how='intersection', keep_geom_type=False) #intersecting region between the two bounding ranges in a gdf
    #df_bounding_box = df[
            #minx, miny, maxx, maxy
     #   (df['latitude'] >= coords[0]-0.0105) & #miny
     #   (df['latitude'] <= coords[0]+0.0105) & #maxy
     #   (df['longitude'] >= coords[1]-0.0105) & #minx
     #   (df['longitude'] <= coords[1]+0.0105) #maxx
     #   ]

   #print('Latmin',coords[0]-0.0105)
   #print('Latmax',coords[0]+0.0105)
   #print('Lonmin',coords[1]-0.0105)
   #print('Lonmax',coords[1]+0.0105)
    #if df_bounding_box.empty:
    if overlap.empty:
        #print('No coordinate data for ',f)
        pass
    else: #if coords exists, get the closest point, LST at the point
        #print(gdf4.bounds)
       # print(gdf_box)
      #  print(overlap)
    #    print(df_bounding_box)
        #print('Contains coordinate data for bounding box.')
        #find coordinate pair closest to ground truth site
        #distances = {} #keys are distances, values are coord pairs
        #for index, row in df_bounding_box.iterrows():
        #for index, row in overlap.iterrows():
        #    lat_comp = row['latitude']
        #    lon_comp = row['longitude']
        #    distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
            #if distance <= 1.125:
            #if distance <= 1.59099026:
        #    distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
        #print('All distances computed.')    
        #coordpair = distances[min(distances)] #this is the closest coordpair
        #print(overlap)
        #print(distances[min(distances)])
        #if min(distances) < 0.375:
        #if min(distances) < 1.125:
        if distances:
            print(distances)
            print(len(distances))
            row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
            LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
            return LST
        
def main():
    #assign user-defined variables
    directory = 'East_Africa/'
    start_date = str(sys.argv[1]) #20180101
    #end_date = str(sys.argv[2]) #201801231
    mid_date = str(sys.argv[2]) #20180630
    start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    #end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
    mid_date_obj = datetime.datetime.strptime(mid_date, '%Y%m%d') #the date you want to stop averaging at, and compare zscore after 
    year = start_date_obj.strftime('%Y')
    start_day = start_date_obj.strftime('%Y%j')
    #end_day = end_date_obj.strftime('%Y%j')
    #mid_day = mid_date_obj.strftime('%Y%j')
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    first_LST = []
    second_LST = []
    #coords = [1.0566795, 34.7679137]

    for f in os.listdir(directory): #loop through East Africa directory, all 2018 files
        date = f[6:13] #2018365
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
            curr_day = datetime.datetime.strptime(date, '%Y%j')
            #print(curr_day)
            if curr_day <= mid_date_obj: #in first half of year
                first_LST.append(LST)
                #print(f, 'first_LST:',LST)
                #print('First:',first_LST)
            #elif curr_day > mid_day:
            else:
                second_LST.append(LST)
                #print(f, 'second_LST:',LST)
                #print('Second:',second_LST)
    
    #once the full list of LST values is gotten for first and second halves
    #get mean from first year, and compute zscores for second half of year against it
    z_scores = calculate_z_scores(np.mean(first_LST), second_LST) 

    #print useful information
    print('Mean of first:' ,np.mean(first_LST))
    print('First:',first_LST)
    print('Second:',second_LST)
    print('z-scores from second:' ,z_scores)

    #make graph of z-scores
    count, bins_count = np.histogram(z_scores, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf)
    #pdf_values = norm.pdf(z_scores)
    #cdf_values = np.cumsum(pdf_values)
    #cdf_values /= cdf_values[-1]  # Normalize the CDF to have a maximum value of 1
    #plt.rcParams["figure.figsize"] = [7.50, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    #plt.plot(z_scores, cdf_values, marker='o')
    plt.xlabel('LST z-scores')
    plt.ylabel('Probabilities')
    plt.title('CDF of Z-Scores of Land Surface Temperature for 2018 at Savanna Pixel')
    plt.grid(True)
    #plt.show()
    plt.savefig(png_filepath + 'zscore_lst_cdf_savanna_pixel_%d.png' % (int(year)))
	
main()
