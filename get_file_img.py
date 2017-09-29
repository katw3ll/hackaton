from http.client import HTTPSConnection
import datetime
import json

import sys

location_latitude = str(sys.argv[1])
location_longitude = str(sys.argv[2])
distance = '100'
min_timestamp = int(sys.argv[3])
max_timestamp = int(sys.argv[4])
date_increment = int(sys.argv[5]) # every 1 hour


def get_vk(latitude, longitude, distance, min_timestamp, max_timestamp):
    get_request =  '/method/photos.search?lat=' + location_latitude
    get_request+= '&long=' + location_longitude
    get_request+= '&count=100'
    get_request+= '&radius=' + distance
    get_request+= '&start_time=' + str(min_timestamp)
    get_request+= '&end_time=' + str(max_timestamp)
    print (get_request)
    local_connect = HTTPSConnection('api.vk.com', 443)
    local_connect.request('GET', get_request)
    return local_connect.getresponse().read()

def timestamptodate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') + ' UTC'


def create_file(location_latitude, location_longitude, distance, min_timestamp, max_timestamp, date_increment):
        print('Starting parse vk..')
        print('location:', location_latitude, location_longitude)
        print('time: from', timestamptodate(min_timestamp), 'to', timestamptodate(max_timestamp))
        file_vk = open('vk_pars_' + location_latitude + location_longitude + '.txt', 'w')
        local_min_timestamp = min_timestamp
        while (1):
            if (local_min_timestamp >= max_timestamp):
                break
            local_max_timestamp = local_min_timestamp + date_increment
            if (local_max_timestamp > max_timestamp):
                local_max_timestamp = max_timestamp
            print(timestamptodate(local_min_timestamp), '-', timestamptodate(local_max_timestamp))
            vk_json = json.loads(
                get_vk(location_latitude, location_longitude, distance, local_min_timestamp, local_max_timestamp))
            for local_i in vk_json['response']:
                if type(local_i) is int:
                    continue
                file_vk.write(local_i['src_big'] + '\n')
            local_min_timestamp = local_max_timestamp
        file_vk.close()


create_file(location_latitude, location_longitude, distance, min_timestamp, max_timestamp, date_increment)
