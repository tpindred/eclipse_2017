from plot_gpx import getGpsPoints
from urllib.request import urlopen
import json
from decimal import *

gpx_file = "eclipse_data_2017.gpx"
start_date = '0818' # 3 days before the eclipse date, Aug 21, in MMDD format
end_date = '0824' # 3 days after the eclipse date, Aug 21, in MMDD format
f = open('wunderground_key.txt')
api_key = f.read()
api_key = api_key.rstrip()

def getCloudyData(lon,lat):
    url = 'http://api.wunderground.com/api/' + api_key + '/planner_' + start_date + end_date + '/q/' + str(lat) + ',' + str(lon) + '.json'
    data = urlopen(url)
    json_string = data.read().decode('utf8')
    parsed_json = json.loads(json_string)
    print(parsed_json)
    partly_cloudy_chance = parsed_json['trip']['chance_of']['chanceofpartlycloudyday']['percentage']
    cloudy_chance = parsed_json['trip']['chance_of']['chanceofcloudyday']['percentage']
    chance_of_clouds = float(partly_cloudy_chance) + float(cloudy_chance)
    return chance_of_clouds

def refineGrid(gpsdata):
    for name, data in gpsdata.items():
        lon_list = data[0]
        lat_list = data[1]
        new_lons = []
        new_lats = []
        for i,lon in enumerate(lon_list):
            if i == len(lon_list)-1:
                new_lons.append(lon)
                new_lats.append(lat_list[i])
                break
            new_lon = (lon + lon_list[i+1])/2
            new_lons.append(lon)
            new_lons.append(new_lon)
            new_lat = (lat_list[i] + lat_list[i+1])/2
            new_lats.append(lat_list[i])
            new_lats.append(new_lat)
        gpsdata[name] = [new_lons,new_lats]
    return gpsdata

def meterRequests(gpsdata):
    request_limit = 5
    for name, data in gpsdata.items():
        lon_list = data[0]
        lat_list = data[1]
        data.append([])
        for i,lon in enumerate(lon_list):
            if i > request_limit-1:
                break
            cloudy_chance = getCloudyData(lon,lat_list[i])
            print(cloudy_chance)
            data[2].append(cloudy_chance)
    return gpsdata
            
def main():
    data = getGpsPoints(gpx_file)
    data = refineGrid(data)
    data = meterRequests(data)

if __name__ == "__main__":
    main()
