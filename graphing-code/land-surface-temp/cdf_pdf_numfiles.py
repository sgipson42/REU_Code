#run as python3 .py start_date=20180101 end_date=20181231
#adjust dates as needed -- currently loops through every day of the yearimport numpy as np
import sys
import glob
import numpy as np
import datetime
import matplotlib.pyplot as plt
#from scipy.stats import gaussian_kde
import scipy.stats as ss

#assign user-defined variables
directory = '/work/pi_jtaneja_umass_edu/sgipson/LST/East_Africa/VNP21.'
start_date = str(sys.argv[1]) #20180101
end_date = str(sys.argv[2]) #20181231
start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
year = start_date_obj.strftime('%Y')
current = start_date_obj
files_per_day = []
png_filepath = '/work/pi_jtaneja_umass_edu/sgipson/LST/graphs/'

#loop through the days
while current <= end_date_obj:
    year_day = current.strftime('%Y%j')
    #get all the files for the day
    files = glob.glob(directory + year_day + '.*.csv')
    #count the files for this day
    num_files = len(files)#y
    #files_per_day.append([num_files, year_day])
    files_per_day.append([num_files])
    #advance loop to next date object
    current += datetime.timedelta(days=1)
print(files_per_day)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
count, bins_count = np.histogram(files_per_day, bins=10)
pdf = count / sum(count)
cdf = np.cumsum(pdf)
plt.plot(bins_count[1:], cdf, label="CDF")
plt.plot(bins_count[1:], pdf, color="red", label="PDF")
plt.xlabel('Number of Files per Day')
plt.ylabel('Probabilities')
plt.title('CDF and PDF for the Number of Files per Day for East Africa 2018')
plt.legend()
plt.savefig(png_filepath + 'cdf_pdf_numfiles_%d_East_Africa.png' % (int(year)))

