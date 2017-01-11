import requests
import json
url = 'https://10.0.0.19/api/1.0/'
D42_USERNAME = 'admin'
D42_PASSWORD = 'adm!nd42'
r = requests.get(url+'rooms', auth=(D42_USERNAME, D42_PASSWORD), verify=False)
data = r.json()
#print ' %s JSON DATA' %entity.upper()

with open('./json/rooms.json', 'w') as f:
    json.dump(data, f)
print 'done'