#curl -v -X POST -d "name=main office&address=123 main st&contact_name=roger&contact_phone=1234567890&notes=super critical" -u 'admin:adm!nd42' 
#https://10.0.0.133/api/1.0/buildings/ --insecure*/

import requests
import json
import base64

url = 'https://10.0.0.19/api/1.0/devices/'
mydict = {'name': 'TXARL1-pworker125'}

print type(mydict)
D42_USERNAME = 'admin'
D42_PASSWORD = 'adm!nd42'

#data_json = json.loads(data_json)
#print data_json
headers = {
            'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD),
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

response = requests.post(url, data=mydict, auth=(D42_USERNAME, D42_PASSWORD),\
                          headers=headers, verify=False)
print(response.status_code, response.reason)

print (response.json())