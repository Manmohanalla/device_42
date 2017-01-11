import requests
import json
import base64
import sys
import argparse
import csv
import os
requests.packages.urllib3.disable_warnings()
url = 'https://10.0.0.19/api/1.0/'
D42_USERNAME = 'admin'
D42_PASSWORD = 'adm!nd42'

def delete(data,entity):
		del_url = 'https://10.0.0.19/api/1.0/'+entity
		headers = {
				'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD),
				'Content-Type' : 'application/x-www-form-urlencoded'
			}
		try:
			response = requests.delete(del_url+data, auth=(D42_USERNAME, D42_PASSWORD),\
								  headers=headers, verify=False)

			response = response.json()
			#print 'posted %s' %entity
			print response
		except Exception as e:
			print e
delete('873/','devices/')