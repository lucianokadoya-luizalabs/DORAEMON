# Import Config Informations
import os
import urllib
import simplejson
import ssl
import ast
import time
import datetime


# Import DB package
from influxdb import InfluxDBClient


org_tmp1 = os.environ['org1']
org_tmp2 = os.environ['org2']

# while True:
while True:

	# mount url 
	org_tmp = org_tmp1
	org_tmp1 = org_tmp2
	org = org_tmp1
	today = datetime.datetime.now()
	d1 = datetime.timedelta(minutes=105)
	d2 = datetime.timedelta(minutes=110)
	begin = today + d1
	end = today + d2
	data_begin = str("timeRange=" + begin.strftime("%m/%d/%Y") + "%20" + begin.strftime("%H:%M"))
	data_end = str(end.strftime("%m/%d/%Y") + "%20" + end.strftime("%H:%M"))
	url1 = os.environ['url_bgn'] + org + os.environ['url_mdn'] + os.environ['slc1'] + os.environ['url_end'] + data_begin + "~" + data_end
	url2 = os.environ['url_bgn'] + org + os.environ['url_mdn'] + os.environ['slc2'] + os.environ['url_end'] + data_begin + "~" + data_end
	print(url1)
	print(url2)

	# API Connection
	url_1 = urllib.request.Request(url1)
	url_1.add_header("Authorization", "Basic %s" % os.environ['pass_api'])
	url_2 = urllib.request.Request(url2)
	url_2.add_header("Authorization", "Basic %s" % os.environ['pass_api'])

	r = urllib.request.urlopen(url_1)
	data = simplejson.load(r)
	r2 = urllib.request.urlopen(url_2)
	data2 = simplejson.load(r2)

	json_data = data['environments'][0]['dimensions']
	json_data2 = data2['environments'][0]['dimensions']
	
	# Find the total of the Itens
	n = sum(1 for line in json_data)

	while n > 0 :
		try:

			result = (json_data[n-1]['metrics'][1]['values'][0])
			result2 = (json_data[n-1]['name'])
			print(result, result2)

			json_body = [
			{
				"measurement": os.environ['slc1'],
				"tags": {
					"proxy": result2
				},
				"fields": {
					"value": result
				}
			}
			]

			result3 = (json_data2[n-1]['metrics'][0]['values'][0])
			print(result3, result2)

			json_body2 = [
			{
				"measurement": os.environ['slc2'],
				"tags": {
					"proxy2": result2
				},
				"fields": {
					"value2": result3
				}
			}
			]
			#print(json_body2)
			client = InfluxDBClient(host=os.environ['host_db'], port=os.environ['port_db'], database=os.environ['base_db'])
			client.create_database(os.environ['base_db'])
			client.write_points(json_body)
			client.write_points(json_body2)

		except urllib.error.HTTPError as err:

			if err.code == 500:
				print("Error = ", err)
				continue

		# Pass to the next Item
		n-=1

	# Time wait until the next search
	time.sleep(float(os.environ['delay']))
	org_tmp2 = org_tmp