#specify pollutant, year, box size and coordinates before running 
#only look at at 2019 json files
	#run for each landcover type
    #run on no2, and co
import os
import sys
import json
import geopandas as gpd
import shapely
from shapely.geometry import Point
from shapely import geometry

directory = '/work/pi_jtaneja_umass_edu/sgipson/pollution/Skyler_NO2/CO/'
pixel_data = [] #if saving to one giant list of days for 2019
year = '2019'

#get the coordinates for the 1km box you want around ground truth point
#make square buffer--500m for a 1km box
coords = [1.0566795, 34.7679137] #forest ground truth coords
p1=Point(34.7679137, 1.0566795)
gdf=gpd.GeoSeries(p1)
gdf.set_crs('EPSG:4326', inplace = True)
gdf2 =gdf.to_crs('EPSG:32733')
gdf3 = gdf2.buffer(2500, cap_style=3)#for a 1km square(1000m) #for a 3km box
gdf4 = gdf3.to_crs('EPSG:4326')
gdf_box = gpd.GeoDataFrame(geometry=gdf4) #1km bounding box

for f in os.listdir(directory): #each file is a month's worth of data
    #if f[4:8] == year: #NO2
    if f[3:7] == year: #CO
        #file = open(directory + 'NO2_2021-07-01_2021-07-31.json')
        filepath = directory + f
        with open(filepath, "r") as file:
            data = json.load(file) #return JSON object as a dictionary
            for i in data['features']: #iterate through the json, list
	        #access and check date/times if needed (not needed for this)
	        #get geometry as a geodataframe
                geom_dict = i['geometry']
                coords = geom_dict['coordinates']
                points = []
                for coord in coords:
                    for coordpair in coord:
                        p = Point(coordpair)
                        points.append(p)
		
                poly=geometry.Polygon(points)
                gdf5 = gpd.GeoSeries(poly)
                gdf6 = gdf5.set_crs('EPSG: 4326')		
                gdf_file = gpd.GeoDataFrame(geometry=gdf6)
	        #check if this geometry intersects the geometry of the dictionary item
                overlap = gdf_box.overlay(gdf_file, how='intersection', keep_geom_type=False)

                if overlap.empty:
                    pass
                else: #if in pixel I want, save item to pixel_data list of dictionary objects
                    props = i['properties']
                    print(props['date'])
                    #print(i)
                    pixel_data.append(i) #giant list of days
			
            #f.close() #close file
    else: #if year is not correct year
        pass

#after looping through each month and year of data: (each json in directory)
filepath = '/work/pi_jtaneja_umass_edu/sgipson/pollution/CO_2019_forest_5x5_area.json'
print(pixel_data)
with open(filepath, 'w') as outfile: #save json file
    json_str = json.dumps(pixel_data)  #convert daily dictionaries for the pixel to a json
    outfile.write(json_str)
