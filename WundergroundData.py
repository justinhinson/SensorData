import urllib2
import json
from influxdb import InfluxDBClient
import credentials as cd
import time as t


usr = cd.usr
password = cd.passwd
db = 'gpstest'
host = cd.host
port = cd.port
measurement = "iaq"
client = InfluxDBClient(host, port, usr, password, db)

try:
	delaytime = raw_input('How much time in between calls?(in seconds)')
except ValueError:
	delaytime = raw_input('Invalid Input! Enter a number:')

delaytime = float(delaytime)

#if isinstance(delaytime, str):
	#delaytime = float(raw_input('Enter a number, not a string:'))

while True:
	url = urllib2.urlopen('http://api.wunderground.com/api/cdcf47b0cf21032c/conditions/q/pws:KNJPRINC11.json')
	json_string = url.read()
	parsed_json = json.loads(json_string)
	location = parsed_json['current_observation']['display_location']['full']
	latitude = float(parsed_json['current_observation']['observation_location']['latitude'])
	longitude = float(parsed_json['current_observation']['observation_location']['longitude'])
	temp = float(parsed_json['current_observation']['temp_c'])
	hum = float(parsed_json['current_observation']['relative_humidity'].strip('%'))
	time = parsed_json['current_observation']['observation_time_rfc822']

	labels = {'latitude':latitude, 'longitude':longitude, 'temp_c':temp, 'relative_humidity':hum}

	for label,value in labels.items():
		json_body = [
			{
				"measurement": measurement,
				"tags": {
					"experiment": 'Wunderground',
					'location': 'Lot 21',
					"label": label,
				},
				"time": time,
				"fields": {
					"value": value,
				}
			}
		]
		print json_body
	   	client.write_points(json_body)
	t.sleep(delaytime)



