#run as sbatch script
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
#adjust dates as needed -- currently loops through every day of the year
#time gap = 0 is no days between samples -- taken on same day
#assign user-defined variables
directory = '/work/pi_jtaneja_umass_edu/sgipson/LST/East_Africa/VNP21.'
year = str(sys.argv[1]) #20180101
time_gaps = []
png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'

#get all the files for the year
files = glob.glob(directory + year + '*.csv')
prev_day = '001'
#loop through files
for f in files:
    filename = f.split('/')[-1]  #'VNP21.2018365.1112.nc'
    #get the current day of the file
    current_day = filename[10:13] #365
    #compare it to the last file day
    diff = int(current_day)-int(prev_day)
    #append the different
    #time_gaps.append([diff, (prev_day+'-'+current_day)])
    time_gaps.append(diff)
    #make current day the last file day for next comparison
    prev_day = current_day

print(time_gaps)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
count, bins_count = np.histogram(time_gaps, bins=10)
pdf = count / sum(count)
cdf = np.cumsum(pdf)
plt.plot(bins_count[1:], cdf, label="CDF")
plt.plot(bins_count[1:], pdf, color="red", label="PDF")
plt.xlabel('Days Between Measurements')
plt.ylabel('Probabilities')
plt.title('CDF and PDF for the Number of Days Between Collected Data for East Africa 2018')
plt.legend()
#plt.show()

#Calculate CDF values for timegaps
#sorted_timegaps = np.sort(time_gaps)
#define x and y values to use for CDF
#x = np.linspace(min(sorted_timegaps), max(sorted_timegaps), 1000)
#y = ss.norm.cdf(x)
#plot normal CDF
#plt.plot(x, y, color='red')
#plt.title('Normal CDF of Days Between Measurements East Africa 2018')
#plt.xlabel('Days Between Measurements')
#plt.ylabel('CDF')

#total_gaps = len(sorted_timegaps)
#cumulative_timegaps = np.cumsum(sorted_timegaps)
#cdf_vals_timegaps = cumulative_timegaps / np.sum(sorted_timegaps)

#plot timegaps CDF
#plt.plot(sorted_timegaps, cdf_vals_timegaps)
#plt.xlabel('Days Between Measurements')
#plt.ylabel('CDF')
#plt.title('CDF of the Gaps in Days Between Measurements for %d in East Africa' % (int(year)))
#plt.grid()
plt.savefig(png_filepath + 'cdf_pdf_timegaps_%d_EastAfrica.png' % (int(year)))
