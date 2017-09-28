from http.client import HTTPSConnection
import datetime
import json

location_latitude = '55.758310'
location_longitude = '37.579982'
distance = '100'
min_timestamp = 1506546000
max_timestamp = 1506718800
date_increment = 60*60*1 # every 1 hour
instagram_access_token = '4124615502.1677ed0.f1c8acc93d3c441cadba9beebb50a514'

""" def get_instagram (latitude, longitude, distance, min_timestamp, max_timestamp, access_token):
    get_request = '/v1/media/search?lat=' + latitude
    get_request += '&lng=' + longitude
    get_request += '&distance=' + distance
    get_request += '&min_timestamp=' + str(min_timestamp)
    get_request += '&max_timestamp=' + str(max_timestamp)
    get_request += '&access_token=' + access_token
    get_request += '&scope=public_content'

    local_connect = HTTPSConnection('api.instagram.com', 443)
    local_connect.request('GET', get_request)
    return local_connect.getresponse().read() """

def get_vk(latitude, longitude, distance, min_timestamp, max_timestamp):
    get_request =  '/method/photos.search?lat=' + location_latitude
    get_request+= '&long=' + location_longitude
    get_request+= '&count=100'
    get_request+= '&radius=' + distance
    get_request+= '&start_time=' + str(min_timestamp)
    get_request+= '&end_time=' + str(max_timestamp)
    local_connect = HTTPSConnection('api.vk.com', 443)
    local_connect.request('GET', get_request)
    return local_connect.getresponse().read()

def timestamptodate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') + ' UTC'

def parse_vk(location_latitude, location_longitude, distance, min_timestamp, max_timestamp, date_increment):
    print ('Starting parse vk..')
    print ('location:',location_latitude,location_longitude)
    print ('time: from',timestamptodate(min_timestamp),'to',timestamptodate(max_timestamp))
    file_vk = open('vk_pars_'+location_latitude+location_longitude+'.html','w')
    file_vk.write('<html>')
    local_min_timestamp = min_timestamp
    while (1):
        if ( local_min_timestamp >= max_timestamp ):
            break
        local_max_timestamp = local_min_timestamp + date_increment
        if ( local_max_timestamp > max_timestamp ):
            local_max_timestamp = max_timestamp
        print (timestamptodate(local_min_timestamp),'-',timestamptodate(local_max_timestamp))
        vk_json = json.loads(get_vk(location_latitude, location_longitude, distance, local_min_timestamp, local_max_timestamp))
        for local_i in vk_json['response']:
            if type(local_i) is int:
                continue
            file_vk.write('<br>')
            file_vk.write('<img src='+local_i['src_big']+'><br>')
            file_vk.write(timestamptodate(int(local_i['created']))+'<br>')
            file_vk.write('http://vk.com/id'+str(local_i['owner_id'])+'<br>')
            file_vk.write('<br>')
        local_min_timestamp = local_max_timestamp
    file_vk.write('</html>')
    file_vk.close()

print (get_vk(location_latitude, location_longitude, distance, min_timestamp, max_timestamp))
parse_vk(location_latitude, location_longitude, distance, min_timestamp, max_timestamp, date_increment)