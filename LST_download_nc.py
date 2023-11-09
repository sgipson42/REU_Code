#modified from downloading script found at https://git.earthdata.nasa.gov/projects/LPDUR/repos/daac_data_download_python/browse/DAACDataDownload.py
from subprocess import Popen
from getpass import getpass
from netrc import netrc
import argparse
import os
import requests
import sys
import datetime
import re

prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
           'Enter NASA Earthdata Login Password: ']
base_url = 'https://e4ftl01.cr.usgs.gov/VIIRS/VNP21.001/'
start_date = str(sys.argv[1])
end_date = str(sys.argv[2])
start_date_obj = datetime.datetime.strptime(start_date, '%Y%m%d')
end_date_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
current_time = start_date_obj
year = current_time.strftime('%Y')
saveDir = '/gypsum/eguide/data/skyler/raw_data/%d/' % (int(year))


if saveDir[-1] != '/' and saveDir[-1] != '\\':
    saveDir = saveDir.strip("'").strip('"') + os.sep
    
urs = 'urs.earthdata.nasa.gov'
try:
    netrcDir = os.path.expanduser("~/.netrc")
    netrc(netrcDir).authenticators(urs)[0]
# Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
except FileNotFoundError:
    homeDir = os.path.expanduser("~")
    Popen('touch {0}.netrc | chmod og-rw {0}.netrc | echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
    Popen('echo login {} >> {}.netrc'.format(getpass(prompt=prompts[0]), homeDir + os.sep), shell=True)
    Popen('echo password {} >> {}.netrc'.format(getpass(prompt=prompts[1]), homeDir + os.sep), shell=True)
# Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
except TypeError:
    homeDir = os.path.expanduser("~")
    Popen('echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
    Popen('echo login {} >> {}.netrc'.format(getpass(prompt=prompts[0]), homeDir + os.sep), shell=True)
    Popen('echo password {} >> {}.netrc'.format(getpass(prompt=prompts[1]), homeDir + os.sep), shell=True)

while (current_time <= end_date_obj):
    date = current_time.strftime('%Y.%m.%d/')
    url = base_url + date
    with requests.get(url, verify=False, stream=True, auth=(netrc(netrcDir).authenticators(urs)[0], netrc(netrcDir).authenticators(urs)[2])) as response:
        if response.status_code == 200:
            txt_data = response.text
            pattern = r'<a href="([^"]+\.nc)">(.*?)<\/a>\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+([\d.]+\w)'
            matches = re.findall(pattern, txt_data)
            for match in matches:
                full_filename = match[0]
                filename = full_filename[0:6] + full_filename[7:19] + full_filename[37:40]
                saveName = os.path.join(saveDir, filename)
                full_url = url + full_filename
                with requests.get(full_url, verify=False, stream=True, auth=(netrc(netrcDir).authenticators(urs)[0], netrc(netrcDir).authenticators(urs)[2])) as response:
                    response.raw.decode_content = True
                    content = response.raw
                    with open(saveName, 'wb') as d:
                	    while True:
                                chunk = content.read(16 * 1024)
                                if not chunk:
                                    break
                                d.write(chunk)

    current_time += datetime.timedelta(days=1)
    
