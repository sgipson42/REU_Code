#in 50km bounding box don't have varous landocver types, but could use for different pixels
#cdf graph code for multipixels, one pollutant graphed
    #run for zscores, then comment out and run for reg cdf
#change poln variable name at each mention of it in code
import sys
import json
import matplotlib.pyplot as plt

def calculate_z_scores(mean, data):
   std_dev = np.std(data)
   z_scores = (data - mean) / std_dev
   return z_scores

def main():
    files = [['no2_2019_forest_pixel.json', 'green', 'Forest'],['no2_2019_savanna_pixel.json', 'red', 'Savanna'], ['no2_2019_agriculture_pixel.json', 'blue', 'Agriculture'], ['no2_2019_nairobi_pixel.json', 'black', 'Nairobi']]
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/pollution/graphs/'
    start_date = str(sys.argv[1]) #2019-01-01
    mid_date = str(sys.argv[2]) #2019-06-30
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    mid_date_obj = datetime.datetime.strptime(mid_date, '%Y-%m-%d')
    year = start_date_obj.strftime('%Y')

    for filename in files: #files for different pixels
        #pixel_conc = []
	first = []
	second = []
	with open(filename[0], 'r') as f:
	    data = json.load(f)
	    for i in data:
	        properties = i['properties']
		conc = properties['no2'] #no2, co
		#need dates for z-score graph
		full_date = properties['date'] #2019-01-01T...
		date = full_date[:10]
		file_year = date[:4]
		if file_year == year: #if data is for correct year, check the month/ day of year to see which list to add conc to (for zscore)
		    #pixel_conc.append(conc) #for regular cdf, not z-scores
		    curr_date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
		    if curr_date_obj <= mid_date_obj: #in first half of year
        	        first.append(conc)
    		    else if curr_date_obj > mid_date_obj: #in second half of year
    		        second.append(conc)
    		else:
    		    pass
    				
        #now that you have pixel_conc, first, and second for a single pixel, graph lines for the pixel
	#get mean from first year, and compute zscores for second half of year against it
	z_scores = calculate_z_scores(np.mean(first), second) 
	
	#print useful information
    	print('Mean of first:' ,np.mean(first))
    	print('First:',first)
    	print('Second:',second)
	print('z-scores from second:' ,z_scores)
	
    	#plot z-scores
    	count, bins_count = np.histogram(z_scores, bins=10)
    	pdf = count / sum(count)
    	cdf = np.cumsum(pdf)
    	plt.plot(bins_count[1:], cdf, color = filename[1], label = filename[2])
    	print('Line plotted.')
    
    	#plot regular CDF
    	#count, bins_count = np.histogram(pixel_conc, bins=10)
        #pdf = count / sum(count)
        #cdf = np.cumsum(pdf)
        #plt.plot(bins_count[1:], cdf, color= filename[1], label= filename[2])
        #print('Line plotted.')
        
    #once all pixels have been plotted--zscore
    plt.xlabel('Z-Scores of NO2 Concentration')
    plt.ylabel('Probabilities')
    plt.title('Z-Score CDF of NO2 Concentration by Landcover Type 2019')
    plt.grid(True)
    plt.legend()
    plt.savefig(png_filepath + 'zscore_NO2_multipixel_2019.png'
    
    #once all pixels have been plotted--regular CDF
    #plt.xlabel('NO2 Concentration')
    #plt.ylabel('Probabilities')
    #plt.title('CDF of NO2 Concentration by Landcover Type 2019')
    #plt.grid(True)
    #plt.legend()
    #plt.savefig(png_filepath + 'cdf_NO2_multipixel_2019.png'
    
main()
