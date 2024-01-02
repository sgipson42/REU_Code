#modified from Colorado Mines VIIRS Nightfires data downloading script
import requests 
import json 
import os
import calendar

# Retrieve access token
params = {    
    'client_id': 'eogdata_oidc', 
    'client_secret': <client_secret>, 
    'username': <username>,
    'password': <password>, 
    'grant_type': 'password' 
} 
token_url = 'https://eogauth.mines.edu/auth/realms/master/protocol/openid-connect/token' 
response = requests.post(token_url, data = params)
access_token_dict = json.loads(response.text) 
access_token = access_token_dict.get('access_token') 

base_url = 'https://eogdata.mines.edu/wwwdata/viirs_products/vnf/v30/rearrange/'
Years = [2018, 2019, 2020, 2021, 2022, 2023]

for year in Years:
    if year == 2023:
        for month in range (1, 7): 
            for day in range (1, (calendar.monthrange(year, month)[1])+1):
	        #Submit request with token bearer
                full_url = base_url + '/%d/%02d/npp/VNF_npp_d%d%02d%02d_noaa_v30.csv.gz' % (year, month, year, month, day)
                auth = 'Bearer ' + access_token 
                headers = {'Authorization' : auth} 
                response = requests.get(full_url, headers = headers)
                #Write response to output file 
                filename = '%d%02d%02d_npp_v30.csv.gz' % (year, month, day)
                output_file = os.path.basename(filename)
                with open(output_file,'wb') as f:
                    f.write(response.content)
    else:	
        for month in range (1, 13):
            for day in range (1, (calendar.monthrange(year, month)[1])+1):
                #Submit request with token bearer
                full_url = base_url + '/%d/%02d/npp/VNF_npp_d%d%02d%02d_noaa_v30.csv.gz' % (year, month, year, month, day)
                auth = 'Bearer ' + access_token 
                headers = {'Authorization' : auth} 
                response = requests.get(full_url, headers = headers)
                #Write response to output file 
                filename = '%d%02d%02d_npp_v30.csv.gz' % (year, month, day)
                output_file = os.path.basename(filename)
                with open(output_file,'wb') as f:
                    f.write(response.content)
					
