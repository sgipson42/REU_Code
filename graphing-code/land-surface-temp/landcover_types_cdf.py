import pandas as pd
import math
import numpy as np
import sys
import datetime
import glob
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

#if __name__ == '__main__':
def main():
    #assign user-defined variables
    directory = 'East_Africa/VNP21.'
    start_date = str(sys.argv[1]) #20180101
    end_date = str(sys.argv[2]) #20181231
    start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
    year = start_date_obj.strftime('%Y')
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'
	
    #make a list of the boundaries and coordinates
    coord_lists = [[1.011106, 37.736814, 'Savanna', 'red'], 
	[0.032167, 37.745747, 'Agricultural Region', 'black'], 
	[1.0566795, 34.7679137, 'Forest', 'green'], 
	[1.287214, 36.823147, 'Nairobi', 'blue']
	]
	
    #set up plot
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.xlabel('Average Land Surface Temperature per Day')
    plt.ylabel('Probabilities')
    plt.title('CDF of Average Land Surface Temperature per Day Across Kenya 2018')
    
    #each file will have a different set of "closest coordinates"--call this method for each file
    for coord_list in coord_lists:
        print(coord_list)
        current = start_date_obj
        daily_LST = []
        while current <= end_date_obj:
            year_day = current.strftime('%Y%j')
            #get all the files for the day
            files = glob.glob(directory + year_day + '.*.csv')
            av_LST = 0
            nan_count = 0 
            for f in files:
                #print(f)
                df = pd.read_csv(f)
                df_bounding_box = df[
                    (df['latitude'] >= (coord_list[0]-0.007)) &
        	    (df['latitude'] <= (coord_list[0]+0.007)) &
        	    (df['longitude'] >= (coord_list[1]-0.007)) &
        	    (df['longitude'] <= (coord_list[1]+0.007))
        	    ]
                if df_bounding_box.empty or (df_bounding_box['LST'].count() == 0): #if dataframe empty or only null values in LST
                    #print ('Bounding box has no relevant data.')
                    LST = math.nan
                    #nan_count +=1
                else: #if usable data exists
                    #print('Contains LST data for bounding box.')
                    distances = {} #keys are distances, values are coord pairs
                    for index, row in df_bounding_box.iterrows():
                        lat_comp = row['latitude']
                        lon_comp = row['longitude']
                        distance = haversine(coord_list[1], coord_list[0], lon_comp, lat_comp)
                        distances[distance] = [lat_comp, lon_comp] #in df_bounding_box
                    #print('All distances computed.')    
                    coordpair = distances[min(distances)] #return the coordpair of min distance as a tuple
                    if min(distances) < 0.750:
                        row_num = (df[(df['latitude'] == coordpair[0]) & (df['longitude'] == coordpair[-1])].index)
                        #LST = df['LST'].values[row_num] #get the LST associated with the row_num in df_bounding_box
                        LST = (df['LST'].iloc[row_num]).item()
                        print(f, LST)
                    else:
                        LST = math.nan #no data within proper range
        	#while in file loop
                if math.isnan(LST):
                    nan_count += 1 #make sure no unused temp files are part of average
                else:
                    av_LST += LST
	    #once total LST gotten for each file in the day
            if (len(files)-nan_count) != 0: 
                av_LST /= (len(files)-nan_count)
    	        #add daily av_LST to the list for the specific location
                print(current, av_LST)
                daily_LST.append(av_LST)
                #print('Average LST for this date added.')
            else:
                pass
                #print('No LST data for this date available at this location.')
    	    #advance loop to next date object
            current += datetime.timedelta(days=1)
            
        #when all days have been looped through, make the cdf of the LSTs, add to the plot
        if daily_LST:
            print(daily_LST)
            count, bins_count = np.histogram(daily_LST, bins=10)
            pdf = count / sum(count)
            cdf = np.cumsum(pdf)
            plt.plot(bins_count[1:], cdf, color= coord_list[3], label=coord_list[2])
            print('Line plotted.')
    
    #add legend and save figure
    plt.legend()
    plt.savefig(png_filepath + 'cdf_lst_landcover_Kenya_pixels_%d.png' % (int(year)))
	
main()
