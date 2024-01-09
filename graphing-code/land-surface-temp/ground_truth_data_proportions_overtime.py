import pandas as pd
import glob
import sys
import datetime
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

#get the files for one week, filter the bounding box and get the closest coord pair in the range
	#add the LST data at the coord pair to the weekly list of LST data
	#weekly list has individual LST values for the coordinate 
#in the weekly list, get the number of fills, temps, and total list length to do computations
	#find the number of usable vs absent data and percents for the weekly list
	
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
    directory = '/work/pi_jtaneja_umass_edu/sgipson/LST/East_Africa/VNP21.'
    start_date = str(sys.argv[1]) #20180101
    end_date = str(sys.argv[2]) #20181231
    start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
    year = start_date_obj.strftime('%Y')
    curr_week = start_date_obj
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
    df_percents = pd.DataFrame(columns = ['Date', 'Percentage of Absent Data', 'Percentage of Usable Data'])
    coords = [1.0566795, 34.7679137]

    #loop through the days
    while curr_week < end_date_obj:
        print(curr_week)
        weekly_data = []
        curr_day = curr_week
        #get all the files for the week
        for day in range (1,7):
            year_day = curr_day.strftime('%Y%j')
            files = glob.glob(directory + year_day + '.*.csv')
            for f in files: #loop through day files
                LST = find_closest_coords(f)
                #df = pd.read_csv(f)
                #df_bounding_box = df[
                 #   (df['latitude'] >= (coords[0]-0.007)) &
                 #   (df['latitude'] <= (coords[0]+0.007)) &
                 #   (df['longitude'] >= (coords[1]-0.007)) &
                 #   (df['longitude'] <= (coords[1]+0.007))
        	 #   ]
               # if df_bounding_box.empty:
                    #print('No coordinate data for ',f)
                 #   pass
                #else: #if bounding box has data
                    #print('Contains LST data for bounding box.')
                    #find coordinate pair closest to ground truth site
                 #   distances = {} #keys are distances, values are coord pairs
                 #   for index, row in df_bounding_box.iterrows():
                 #       lat_comp = row['latitude']
                 #       lon_comp = row['longitude']
                 #       distance = haversine(coords[1], coords[0], lon_comp, lat_comp)
                 #       distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
                    #print('All distances computed.')    
                 #   coordpair = distances[min(distances)] #this is the closest coordpair
                 #   if min(distances) < 0.750: 
                 #       row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
                 #       LST = (df['LST'].iloc[row_num]).item()#get the LST associated with the row_num of the coordpair in df_bounding_box
                    #save the LST value to the weekly_list, whether it is nan or usable temp
                        weekly_data.append(LST) #but only save it if it is within proper distance
                    #print(LST, f)

            curr_day += datetime.timedelta(days=1) #go to next day
		
        #assign date
        month = curr_week.strftime('%m')
        day = curr_week.strftime('%d')
        date = month + '-' + day
        #calculate variables for percentages
        #print(weekly_data) #each is a dataframe LST column
        series = pd.Series(weekly_data)
        temp_count = series.count()
        fill_count = len(series)-temp_count
        print('date:',date, 'temps:',temp_count, 'fills:',fill_count, 'length:',len(series))
        print(series)
    
        if len(series) != 0:
            temp_percent = (temp_count/len(series)) * 100
            fill_percent = (fill_count/len(series)) * 100

            #add variables to the dataframe (only for days where there is any LST info available)
            df_row = {'Date' : date, 'Percentage of Absent Data' : fill_percent, 'Percentage of Usable Data' : temp_percent}
            df_percents = pd.concat([df_percents, pd.DataFrame([df_row])], ignore_index = True)

        #advance loop to next week
        curr_week += datetime.timedelta(days=7)

    #plot graph
    print('plotting graph.')
    print(df_percents)
    ax = df_percents.plot(x = 'Date', y = ['Percentage of Absent Data', 'Percentage of Usable Data'], kind = "bar", title = "Proportion of Weekly Usable Data for LST at Ground Truth Site 2019", color = ['grey', 'goldenrod'], rot = 45)
    print('graph plotted.')
    fig = ax.get_figure()
    print('figure gotten.')
    fig.set_figwidth(17)
    fig.savefig('/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/%d_LST_weekly_proportions_ground_truth.png' % (int(year)))
    print('figure saved.')
    #fig = ax.get_figure()
main()

#BELOW:
#adjust dates as needed
	#currently loops through every day in the year
	#could do by week instead
		#make a mini loop for seven times, advance it daily and outer loop weekly
		#make sure that never passes end_date
		
##loop through the days
#while current <= end_date_obj:
	#get all the files for the day
#	files = glob.glob(directory + year_day + '.*.csv')
#	for f in files:
#	month = date_obj.strftime('%m')
#	day = date_obj.strftime('%d')
#	date = month + '-' + day
#	df = pd.read_csv(f)
#	filename = file.split('/')[-1] #saves with hours_mins.csv
#	LST = df['LST'] #column of temp values for multiple coords in a day
#	temp_count = LST.count() #num of not null values
#	fill_count = len(LST) - LST.count()
#	temp_percent = (temp_count/len(LST)) *100 #16.71866340825123  
#	fill_percent = (fill_count/len(LST)) *100 #83.28133659174877
	
	#add variables to the dataframe
#	df_row = {'Date' : date, 'Percentage of Absent Data' : fill_count, 'Percentage of Usable Data' : temp_count}
#	df = pd.concat([df, pd.DataFrame([df_row])], ignore_index = True)
	
	#advance loop
#	current += datetime.timedelta(days=1)

#plot graph
#ax = df_temp.plot(x = 'Date', y = ['Percentage of Absent Data', 'Percentage of Usable Data'], kind = "bar", title = "Proportion of Usable Data for LST in East Africa", rot = 45)



