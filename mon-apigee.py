# Import Config Informations
import os
import urllib
import simplejson
import ssl
import ast
import time
import datetime
import sys

# Import DB package
from influxdb import InfluxDBClient

org_tmp1 = os.environ['org1']
org_tmp2 = os.environ['org2']

def mount_json(a, b):
	result = (json_data[n-1]['metrics'][a]['values'][0])
	result2 = (json_data[n-1]['name'])
	print(result, result2)

	# mount json1
	mount_json.body = [
	{
		"measurement": b,
		"tags": {
			"proxy": result2
		},
		"fields": {
			"value": result
		}
	}
	]
	
# Looping
while True:

	# define org 
	org_tmp = org_tmp1
	org_tmp1 = org_tmp2
	org = org_tmp1

	# calcule time range
	today = datetime.datetime.now()
	d1 = datetime.timedelta(minutes=-15)
	d2 = datetime.timedelta(minutes=-10)
	begin = today + d1
	end = today + d2

	# mount url's 
	data_begin = str("timeRange=" + begin.strftime("%m/%d/%Y") + "%20" + begin.strftime("%H:%M"))
	data_end = str(end.strftime("%m/%d/%Y") + "%20" + end.strftime("%H:%M"))

	url_begin = urllib.parse.urljoin(os.environ['url_bgn'], org + os.environ['url_mdn'])
	url_end = os.environ['url_end'] + data_begin + "~" + data_end

	for i in range(2):
		slc3 = 'slc' + str(i)
		env = os.environ[slc3]
		url = url_begin + env + url_end
		print(url)

		# API connection
		url_1 = urllib.request.Request(url)
		url_1.add_header("Authorization", "Basic %s" % os.environ['pass_api'])

		try:
			r = urllib.request.urlopen(url_1)
			data = simplejson.load(r)
		except :
			print("Unexpected error:", sys.exc_info()[0])
			continue

		json_data = data['environments'][0]['dimensions']

	
		# Find the total of the Itens
		n = sum(1 for line in json_data)

		while n > 0 :

			if env == os.environ['slc0']:
				mount_json(1, os.environ['slc0'])
			else:
				mount_json(0, os.environ['slc1'])

			# input data to database
			client = InfluxDBClient(host=os.environ['host_db'], port=os.environ['port_db'], database=os.environ['base_db'])
			#client.create_database(os.environ['base_db'])
			client.write_points(mount_json.body)

			# Pass to the next Item
			n-=1

	# Time wait until the next search
	time.sleep(float(os.environ['delay']))

	# Switch to another org
	org_tmp2 = org_tmp