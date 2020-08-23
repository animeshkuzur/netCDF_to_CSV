from netCDF4 import Dataset
import numpy as np
from datetime import datetime
import os
import shutil
import csv

def get_min_index(data):
	min_val = data[0]
	for val in data:
		if val <= min_val:
			min_val = val
	for i,val in enumerate(data):
		if min_val == val:
			break
	return i	

def get_all_files(folder):
	files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
	return files 

def get_csv_headers(file):
	nc = Dataset(folder+"/"+file, 'r')
	return ["Date",nc.variables['precipitation'].long_name+" ("+nc.variables['precipitation'].units+")",nc.variables['precipitation_cnt'].long_name+" ("+nc.variables['precipitation_cnt'].units+")",nc.variables['IRprecipitation'].long_name+" ("+nc.variables['IRprecipitation'].units+")",nc.variables['IRprecipitation_cnt'].long_name+" ("+nc.variables['IRprecipitation_cnt'].units+")",nc.variables['HQprecipitation'].long_name+" ("+nc.variables['HQprecipitation'].units+")",nc.variables['HQprecipitation_cnt'].long_name+" ("+nc.variables['HQprecipitation_cnt'].units+")"]

def parse_CDF(file,lat_loc,lon_loc):
	#reading the netCRF file
	nc = Dataset(folder+"/"+file, 'r')

	#storing the all values of latitute and longitute in 'lat' and 'lon' variables
	lat = nc.variables['lat'][:]
	lon = nc.variables['lon'][:]

	#get the data of the place based off those co-ordinates
	sq_diff_lat = (lat - lat_loc)**2
	sq_diff_lon = (lon - lon_loc)**2

	lat_index = get_min_index(sq_diff_lat)
	lon_index = get_min_index(sq_diff_lon)

	date = nc.BeginDate

	return [date,nc.variables['precipitation'][lon_index,lat_index],nc.variables['precipitation_cnt'][lon_index,lat_index],nc.variables['IRprecipitation'][lon_index,lat_index],nc.variables['IRprecipitation_cnt'][lon_index,lat_index],nc.variables['HQprecipitation'][lon_index,lat_index],nc.variables['HQprecipitation_cnt'][lon_index,lat_index]]

#path to the input folder
folder = "input_data/"
files = get_all_files(folder)

#Co-ordinates of the place you wish to extract data of
lat_loc = 23.1
lon_loc = 84.96
name_loc = "Lapung"

#creating a new folder with the location name to write the CSV file
if os.path.exists(name_loc):
    shutil.rmtree(name_loc)
os.makedirs(name_loc)

with open(name_loc+'/data.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	data = get_csv_headers(files[0])
	writer.writerow(data)

for file in files:
	# Writing data into CSV file
	with open(name_loc+'/data.csv', 'a', newline='') as f:
	    writer = csv.writer(f)
	    data = parse_CDF(file,lat_loc,lon_loc)
	    writer.writerow(data)

print("Done.")
exit()