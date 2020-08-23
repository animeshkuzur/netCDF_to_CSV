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

def reformat(date):
	date_object = datetime.strptime(date, "%Y-%m-%d")
	return date_object.strftime("%Y-%m-%d")


#path to the file
file = "input_data/"


#reading the netCRF file
nc = Dataset(file, 'r')


#storing the all values of latitute and longitute in 'lat' and 'lon' variables
lat = nc.variables['latitude'][:]
lon = nc.variables['longitude'][:]


#Co-ordinates of the place you wish to extract data of
lat_loc = 28.644800
lon_loc = 77.216721
name_loc = "New Delhi"


#get the data of the place based off those co-ordinates
sq_diff_lat = (lat - lat_loc)**2
sq_diff_lon = (lon - lon_loc)**2

lat_index = get_min_index(sq_diff_lat)
lon_index = get_min_index(sq_diff_lon)


#generating date range from netCDF File
start_date = nc.variables['time'].units[11:19]
start_date = reformat(start_date)

end_date = nc.variables['time'].units[11:16]+"12-31"
end_date = reformat(end_date)

date_range = np.arange(np.datetime64(start_date), np.datetime64(end_date))


#creating a new folder with the location name to write the CSV file
if os.path.exists(name_loc):
    shutil.rmtree(name_loc)
os.makedirs(name_loc)


# Writing data into CSV file
with open(name_loc+'/'+nc.variables['time'].units[11:15]+'.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", nc.variables['precip'].long_name])
    for i,date in enumerate(date_range):
    	writer.writerow([date, nc.variables['precip'][i,lat_index,lon_index]])	

print("Done.")
exit()