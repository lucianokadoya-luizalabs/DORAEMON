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

# Looping
while True:

	# define org 
	org_tmp = org_tmp1
	org_tmp1 = org_tmp2
	org = org_tmp1

	# calcule time range
	today = datetime.datetime.now()
	d1 = datetime.timedelta(minutes=15)
	d2 = datetime.timedelta(minutes=10)
	begin = today - d1
	end = today - d2

	# mount url's 
	data_begin = str("timeRange=" + begin.strftime("%m/%d/%Y") + "%20" + begin.strftime("%H:%M"))
	data_end = str(end.strftime("%m/%d/%Y") + "%20" + end.strftime("%H:%M"))
	url1 = urllib.parse.urljoin(os.environ['url_bgn'], org + os.environ['url_mdn']) + os.environ['slc1'] + os.environ['url_end'] + str(data_begin) + "~" + str(data_end)
	url2 = urllib.parse.urljoin(os.environ['url_bgn'], org + os.environ['url_mdn']) + os.environ['slc2'] + os.environ['url_end'] + data_begin + "~" + str(data_end)
	print(url1)
	print(url2)

	# API connection
	url_1 = urllib.request.Request(url1)
	url_1.add_header("Authorization", "Basic %s" % os.environ['pass_api'])
	url_2 = urllib.request.Request(url2)
	url_2.add_header("Authorization", "Basic %s" % os.environ['pass_api'])

	try:
		r = urllib.request.urlopen(url_1)
		data = simplejson.load(r)
	except urllib.error.HTTPError as err:
		print("except ERROR =", err)
		continue
	try:
		r2 = urllib.request.urlopen(url_2)
		data2 = simplejson.load(r2)
	except urllib.error.HTTPError as err:
		print("except ERROR =", err)
		continue
	json_data = data['environments'][0]['dimensions']
	json_data2 = data2['environments'][0]['dimensions']
	
	# Find the total of the Itens
	n = sum(1 for line in json_data)

	while n > 0 :
		try:
			# parse results
			result = (json_data[n-1]['metrics'][1]['values'][0])
			result2 = (json_data[n-1]['name'])
			print(result, result2)

			# mount json1
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

			# input data to database
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

	# Switch to another org
	org_tmp2 = org_tmp