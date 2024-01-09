#z-score CDF for 3x3 grid--one daytime, and one nighttime as separate graphs
#daytime first if 7<=hour<=19:
#nighttime if hour<7 or hour>19:
import sys
import math
import os
import datetime
import glob
import geopandas as gpd
import shapely
from shapely.geometry import Point, Polygon
from shapely import geometry
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import radians, cos, sin, asin, sqrt

def calculate_z_scores(mean, data):
    std_dev = np.std(data)
    z_scores = (data - mean) / std_dev
    return z_scores

#def find_closest_coords(f):
#    coords = [1.0566795, 34.7679137] #forest ground truth coords
#    p1=Point(34.7679137, 1.0566795)
#    gdf=gpd.GeoSeries(p1)
#    gdf.set_crs('EPSG:4326', inplace = True)
#    gdf2 =gdf.to_crs('EPSG:32733')
#    gdf3 = gdf2.buffer(1125, cap_style=3)#square where 1125 is half the length
#    gdf4 = gdf3.to_crs('EPSG:4326')
#    gdf_box = gpd.GeoDataFrame(geometry=gdf4) #2250m box with point as center
#    df = pd.read_csv(f)
#    gdf_granule = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326')) #East Africa bounding box from file
#    overlap = gpd.sjoin(gdf_box, gdf_granule, how='left', predicate = 'intersects', keep_geom_type=False) #intersecting region between the two bounding ranges in a gdf

#    if overlap.empty:
#        pass
#    else: #if coords exists, get the closest point, LST at the point
#        LST_multipixel = [] #add in order of geometries if possible?
#        points = [df.geometry] #make a list of points
        #poly = geometry.Polygon([[p.x, p.y] for p in points]) #make polygon from the points list
#        for index, row in overlap.iterrows():
#            lst_multipixel.append([row['LST'], row['geometry']]) #add LST value and respective points to list

#        return LST_multipixel

#def_find_closest_coords(f):

#change second_directory filepath to be on gypsum        
def main():
    #assign user-defined variables
    first_directory = 'East_Africa/' #2018 data
    second_directory = '/gypsum/eguide/data/skyler/'
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    first_lst_pixels = {}
    second_lst_pixels = {}
    zscore_pixels = {}
    first_gdfs = []
    second_gdfs = []

    min_lon, min_lat, max_lon, max_lat = 34.75833886, 1.04704232, 34.77748859, 1.0663178 #from gdf.total_bounds of one ground truth pixel
    grid_size_degrees = (max_lon - min_lon) / 3
    pixel_geometries = []
    for i in range(3): #number of pixels in x direction
        for j in range(3): #number of pixels in y direction
            minx = min_lon + i * grid_size_degrees
            maxx = min_lon + (i + 1) * grid_size_degrees
            miny = min_lat + j * grid_size_degrees
            maxy = min_lat + (j + 1) * grid_size_degrees
            pixel_geometry = Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)])
            pixel_geometries.append(pixel_geometry)
        
    # Create the new GeoDataFrame for the pixel grid
    pixel_gdf = gpd.GeoDataFrame(geometry=pixel_geometries, crs= 'EPSG:4326')
    
    for f in os.listdir(first_directory): #loop through East Africa directory, all 2018 files
        if os.path.isfile(first_directory + f):
            date = f[6:13] #2018365
            day = f[10:13]
            if int(day) < 182: #first half of year
            #if int(day) < 10: #first half of year
                hour = int(f[14:16])
                print(hour)
                if 7<=hour<=19: #for daytime LST graph
                    df = pd.read_csv(first_directory + f)
                    granule_gdf= gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326'))
                    overlap = gpd.sjoin(pixel_gdf, granule_gdf, how='left', predicate = 'intersects')

                    if overlap['LST'].count() > 0: #if readable LST values exist
                        #new_gdf = gpd.GeoDataFrame(overlap, columns = ['geometry', 'LST'], crs=overlap.crs)
                        new_gdf = gpd.GeoDataFrame({'geometry': overlap['geometry'], 'LST': overlap['LST']}, crs=overlap.crs)
                        first_gdfs.append(new_gdf) 
            else:
                pass
    sorted_file_names = sorted(os.listdir(second_directory))
    #for f in os.listdir(second_directory): #loop through 2019 East Africa directory, all 2019 files
    for f in sorted_file_names: #loop through 2019 East Africa directory, all 2019 files
        if os.path.isfile(second_directory + f):
            date = f[6:13] #2018365
            print(f)
            day = f[10:13]
            if int(day) < 182: #first half of year
            #if int(day) < 10: #first half of year
                hour = int(f[14:16])
                print(hour)
                if 7<=hour<=19: #for daytime LST graph
                    df = pd.read_csv(second_directory + f)
                    granule_gdf= gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude'], crs = 'EPSG:4326'))
                    overlap = gpd.sjoin(pixel_gdf, granule_gdf, how='left', predicate = 'intersects')

                    if overlap['LST'].count() > 0: #if readable LST values exist
                        new_gdf = gpd.GeoDataFrame({'geometry': overlap['geometry'], 'LST': overlap['LST']}, crs=overlap.crs)
                        second_gdfs.append(new_gdf)  
            else:
                pass
    
    #once both years have been loop through and gdf lists are complete
    #get each list into a dictionary format where pixels are keys and values are LSTs for the pixel
    for gdf in first_gdfs:
        for index, row in gdf.iterrows():
            polygon = row['geometry']
            lst = row['LST']  # Replace 'LST' with your actual column name
            if np.isnan(lst): 
                pass
            else:
                if polygon in first_lst_pixels:
                    first_lst_pixels[polygon].append(lst)
                else:
                    first_lst_pixels[polygon] = [lst]

    for gdf in second_gdfs:
        for index, row in gdf.iterrows():
            polygon = row['geometry']
            lst = row['LST']  # Replace 'LST' with your actual column name
            if np.isnan(lst):
                pass
            else:
                if polygon in second_lst_pixels:
                    second_lst_pixels[polygon].append(lst)
                else:
                    second_lst_pixels[polygon] = [lst]


    #loop through the keys of the dictionary first_lst_pixels, and calculate the z-score for each values list
    palette = sns.color_palette("colorblind")
    #color_legend = [['1', palette[0]], ['2', palette[1]], ['3', palette[2]], ['4', palette[3]], ['5', palette[4]], ['6', palette[5]], ['7', palette[6]], ['8', palette[7]], ['9', palette[9]]]
    ind = 0
    for key in first_lst_pixels.keys():
        first_list = first_lst_pixels[key]
        second_list = second_lst_pixels[key]
        #get mean from first year, and compute zscores for year against it
        z_scores = calculate_z_scores(np.mean(first_list), second_list) 

        #print useful information
        print('Mean of first:' ,np.mean(first_list))
        print('First:',first_list)
        print('Second:',second_list)
        print('z-scores from second:' ,z_scores)

        #make graph of z-scores
        count, bins_count = np.histogram(z_scores, bins=10)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        plt.plot(bins_count[1:], cdf, color = palette[ind], label = ind+1, linewidth=2)
        #plt.hist(bins[:-1], bins, weights=hist, alpha=0.6, color=colors[i], label=key)

        ind += 1    
        #after each line is plotted, show legend and save fig
        #if count == 8:
    plt.legend(title = 'Pixel Number')
    plt.xlabel('LST z-scores')
    plt.ylabel('Probabilities')
    plt.title('CDF of LST Z-Scores Near Ground Truth Site 2018-2019')
    plt.grid(True)
    plt.savefig(png_filepath + 'zscore_lst_cdf_multipixel_pixel_2019_colorblind.png')
        #else :
            #pass
	
main()
