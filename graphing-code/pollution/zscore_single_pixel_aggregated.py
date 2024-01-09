#cdf z-score graph code for one pixel, both pollutants graphed
#adjust dates, filenames, graph title, png title
import sys
import json
import numpy as np
import seaborn as sns
import datetime
import matplotlib.pyplot as plt

def calculate_z_scores(mean, data):
    std_dev = np.std(data)
    z_scores = (data - mean) / std_dev
    return z_scores

def main():
    files = [['no2', 'NO2_2019_forest_5x5_area.json'], ['co', 'CO_2019_forest_5x5_area.json']]
    png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/pollution/graphs/'
    start_date = str(sys.argv[1]) #2019-01-01
    mid_date = str(sys.argv[2]) #2019-06-30
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    mid_date_obj = datetime.datetime.strptime(mid_date, '%Y-%m-%d')
    year = start_date_obj.strftime('%Y')
    first_no2 = []
    second_no2 = []
    first_co = []
    second_co = []
	
    for filename in files: #no2 file, co file
        poln = filename[0] #no2, co
        with open(filename[1], 'r') as f:
            data = json.load(f)
            for i in data:
                properties = i['properties']
                conc = properties[poln] #no2, co
                full_date = properties["date"] #2019-01-01T...
                date = full_date[:10]
                file_year = date[:4]
                if file_year == year: #if data is for correct year, check the month/ day of year to see which list to add conc to
                    curr_date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                    if curr_date_obj <= mid_date_obj: #in first half of year
                        if poln == 'no2': #add to no2 if no2
                            first_no2.append(conc)
                        else: #add to co if not no2
                            first_co.append(conc)
 
                    elif curr_date_obj > mid_date_obj: #in second half of year
                        if poln == 'no2':
                            second_no2.append(conc)
                        else:
                            second_co.append(conc)
                else:
                    pass

    #get mean from first year, and compute zscores for second half of year against it
    z_scores_no2 = calculate_z_scores(np.mean(first_no2), second_no2) 
    z_scores_co = calculate_z_scores(np.mean(first_co), second_co)
	
    #print useful information
    print('NO2:')
    print('Mean of first:' ,np.mean(first_no2))
    print('First:',first_no2)
    print('Second:',second_no2)
    print('z-scores from second:' ,z_scores_no2)
	
    print('CO:')
    print('Mean of first:' ,np.mean(first_co))
    print('First:',first_co)
    print('Second:',second_co)
    print('z-scores from nighttime second:' ,z_scores_co)
    
    colorblind_palette = sns.color_palette("colorblind")
    #plot no2 z-scores
    count, bins_count = np.histogram(z_scores_no2, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label = 'NO2', color = colorblind_palette[0])
    #plot co zscores
    count, bins_count = np.histogram(z_scores_co, bins=10)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label = 'CO', color = colorblind_palette[1])
    plt.xlabel('Z-Scores of Pollutant Concentrations')
    plt.ylabel('Probabilities')
    plt.title('Z-Score CDF of Pollutant Concentrations at Ground Truth Area 2019')
    plt.grid(True)
    plt.legend()
    plt.savefig(png_filepath + 'zscore_pollution_forest_aggregated_2019.png')

main()
