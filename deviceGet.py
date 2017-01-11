import requests
import json
import base64
import sys
import argparse
import csv
import os
from os import listdir
from os.path import isdir, isfile, join
import logging
import glob,shutil,datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime
start=datetime.now()
requests.packages.urllib3.disable_warnings()
url = 'https://192.168.2.60/api/1.0/'
D42_USERNAME = 'admin'
D42_PASSWORD = 'adm!nd42'
base_path = "./json/"
sub = 'Message from device42'
# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="deviceGet.log", level=logging.INFO)
# create log handler and set level to debug
lh = logging.StreamHandler()
lh = logging.FileHandler("deviceGet.log")
lh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to lh
lh.setFormatter(formatter)

# add lh to logger
logger.addHandler(lh)

# create console handler and set level to debug
consoleHandler = logging.StreamHandler()
# add formatter to consolehandler
consoleHandler.setFormatter(formatter)
# add console to logger
logger.addHandler(consoleHandler)



class restfull(object):
	
	def __init__(self):
		
		self.url = url
		self.D42_USERNAME = D42_USERNAME
		self.D42_PASSWORD = D42_PASSWORD
		self.base_path = base_path
		self.sub = sub
	
	def look_files(self):
		src = '/Users/barewolf/projects/device42/drop_csv/'
		#Notes
		os.chdir(src)
		for file in glob.glob('*'):
			if file.endswith(".csv"):
				msg = '%s file found' %file
				logging.info(msg)
				#self.data_caching(src+file)
			else:
				self.move_files(file,src)
		
	def move_files(self,file,src):     
		#Get rid of hardcoding
		#Read from cfg files
		dst = '/Users/barewolf/projects/device42/archive/'  
		chname = str(datetime.datetime.now())+file
		shutil.move(src+file,dst+chname)
		msg = '%s found and moved to archive folder' %file
		logging.warning(msg)

	def csv_validator(self,filename):
		try:
			
			data = (csv.DictReader(open(filename)))
		except Exception as e:
			print e,'hi'
			return
		#name = in service
		header = [name.lower() for name in data.fieldnames]
		print header
		required_headers = ['name','in_service','hardware','rack','id']
		x = [i for i, j in zip(header, required_headers) if i == j]
		
		if not all(item in set(header) for item in set(required_headers)):
			msg= 'Required header/headers missing'
			logger.warning(msg)
			self.email(msg+' at '+str(datetime.datetime.now()))
		else:
			msg = 'All the required headers are found in current csv'
			logger.info(msg)
		
	def email(self,message):
		
	
		fromaddr = "sendmanmohan@gmail.com"
		toaddr = "sendmanmohan@gmail.com"
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = sub
		 
		body = message
		msg.attach(MIMEText(body, 'plain'))
		 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		password = base64.b64decode("Y2FzdGxlMjA0MCMj")
		server.login(fromaddr, password)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
	def parse_arg(self):
		
		parser = argparse.ArgumentParser(prog='PROG')
		parser = argparse.ArgumentParser(description='This program is used to pass different entities to Device42 from a CSV file, Format: --services --name')
		#parser.add_argument('service', help="Get or Post", type=str)
		parser.add_argument('--service', nargs = 2, dest = 'service', help = 'Get or Post or update And give entity (2 Arg)', default = argparse.SUPPRESS)
		parser.add_argument('-name', help="If Get pass entity. If Post pass Filename", type=str)
		args = parser.parse_args()
		service = args.service
		s = service[0].lower()
		a = service[1]
		entity = a.lower()
		
		if s == 'get':
			result = self.get_data(entity)
			#print result
		elif s == 'post' :
			file_name = args.name.lower()
			try:
				
				csv_data = self.parse_csv(file_name, a)
				#print csv_data
		
			except Exception:
				print 'Please give file name Argument to import'
				sys.exit(1) 
		elif s == 'update':
			file_name = args.name.lower()
			result = self.update(file_name, a)
			#data = self.get_data(entity)
			#data = data['Devices']
			#for i in data:
				#i['name']
			#print data
			
		else:
			print 'Please check the services ur looking for'
	def get_json(self):
		
		
		files = listdir(base_path)
		list_files = ['devices.json','rooms.json','racks.json','hardwares.json','buildings.json','devicesall.json']
		for file in list_files:
			if file not in files:
				path = file.split(".json")[0]
				if path=='devicesall':
					path='devices/all/'
				r = requests.get(url+path, auth=(D42_USERNAME, D42_PASSWORD), verify=False)
				data = r.json()
				with open(base_path+file, 'w') as f:
					json.dump(data, f)
			else:
				
				print file
	
	def load_json(self,file_name):

		jdata = json.loads(open (base_path+file_name).read())
		return jdata

	def data_caching(self,data,entity):

		post_rack=False
		if entity =='devices/':
			key = 'Devices'
			key_file='devices.json'
			jdata=self.load_json(key_file)
			jdata = jdata[key]

		elif entity == 'hardwares/':
			key_file='hardwares.json'
			jdata=self.load_json(key_file)
			key='models'
			jdata = jdata[key]

		elif entity == 'racks/':
			key_file='racks.json'
			jdata=self.load_json(key_file)
			jroom = self.load_json('rooms.json')
			jbuilding = self.load_json('buildings.json')
			for i in data:
				if i['room'] not in jroom:
					return 'Add room before rack'
				if i['building'] not in jbuilding:
					return 'Add building and room before adding rack'
			key='racks'
			jdata = jdata[key]

		elif entity == 'rooms/':
			key_file='rooms.json'
			jdata=self.load_json(key_file)
			jbuilding = self.load_json('buildings.json')
			for i in data:
				if i['building'] not in jbuilding:
					return 'Add building and room before adding rack'
			key='rooms'
			jdata = jdata[key]
		elif entity == 'buildings/':
			key_file='buildings.json'
			jdata=self.load_json(key_file)
			key='buildings'
			jdata = jdata[key]
		elif entity == 'device/rack/':
			key='Devices'
			key_file='devicesall.json'
			jdata = self.load_json('racks.json')
			jdata= jdata['racks']
			jdevicesall=self.load_json(key_file)
			jdevicesall = jdevicesall[key]
			for i in data:
				rack = [r['name'] for r in jdata]
				if i['rack'] not in rack:
					return 'add rack before adding device to rack %s' %i['rack_id']
				i['name'] = i['device']
				devices=[d['name'] for d in jdevicesall]
				if i['name'] not in devices:
					return '%s device not found.' %i['name']
				post_rack=True

		else:
			sys.exit(1)
		
		for i in data:

			if i not in jdata:
				if i['name'] in [names['name'] for index,names in enumerate(jdata)]:
					r=self.put_data(i,entity)
					jdata[index] = i
					dic = {key:jdata}
					with open(base_path+key_file, 'w') as f:
						json.dump(dic, f)
				elif post_rack==False:
					response = self.post_data(i,entity) 
					if response==200:
						jdata.append(i)
						dic = {key:jdata}
						with open(base_path+key_file, 'w') as f:
							json.dump(dic, f)
			if post_rack:
				response = self.post_data(i,entity)
				if response == 200:
					index = next(index for index,name in enumerate(jdevicesall) if i['device'] == name['name'])
					jdevicesall[index]['rack']=i['rack']
					dic = {key:jdevicesall}
					#print dic
					with open(base_path+key_file,'w') as f:
						json.dump(dic, f)

		return data
		
	def update(self,file_name,entity):
		path =entity.lower()
		if os.stat('deviceHardlog.csv').st_size!=0:

			csv1 = (csv.DictReader(open('deviceHardlog.csv')))
			csv2 = (csv.DictReader(open(file_name)))
			
			csv1.fieldnames = [name.lower() for name in csv1.fieldnames]
			csv2.fieldnames = [name.lower() for name in csv2.fieldnames]
			csv1=list(csv1)
			csv2=list(csv2)
			for row in csv1:

				if row not in csv2 and row['id'] not in [x['id'] for x in csv2]: 
					for key in row.keys():
						if row[key].lower() == 'true':
							row[key] = 'yes'
							#print row[key]
						elif row[key].lower() == 'false':
							row[key] = 'no'
					r=self.delete(row['id'],path)
					type(row)
			for row in csv2:
				
				if row not in csv1:
					for key in row.keys():
						if row[key].lower() == 'true':
							row[key] = 'yes'
							#print row[key]
						elif row[key].lower() == 'false':
							row[key] = 'no'
					r=self.post_data(row,path)
					with open('deviceHardlog.csv', 'w') as csvoutput:
						writer = csv.writer(csvoutput)
						writer.writerow(list(row))
		else:
			self.parse_data(file_name,entity)

	def parse_csv(self,file_name,entity):
		
		reader = csv.DictReader(open(file_name, 'rb'))
		reader.fieldnames = [name.lower() for name in reader.fieldnames]
		ls = []
		for line in reader:
			ls.append(line)
			for key in line.keys():
				if line[key].lower() == 'true':
					line[key] = 'yes'
					#print row[key]
				elif line[key].lower() == 'false':
					line[key] = 'no'
		self.parse_data(ls,entity)

	def parse_data(self,dic,entity):
		path = entity.lower()
		data = self.get_data(path)
		get_entity =entity[:-1]
		devices=[]
		data = data[get_entity]
		for device in data:
			devices.append(device['name'])

		hardwares = self.get_data('hardwares/')
		rooms = self.get_data('rooms/')
		racks =self.get_data('racks/')
		buildings =self.get_data('buildings/')

		hardwares= hardwares['models']
		rooms= rooms['rooms']
		racks= racks['racks']
		buildings =buildings['buildings']           
		hard={}
		room_dic={}
		rack_dic={}
		build_dic={}
			
		hardware_names = [i['name'] for i in hardwares]
		room = [i['name'] for i in rooms]
		rack = [i['name'] for i in racks]
		build = [i['name'] for i in buildings]
		hardware_names.append('None')
		rack.append('None')
		room.append('None')
		build.append('None')

		for item in dic :
			
					
			if item['hardware'] not in hardware_names:
					
					#print item['hardware']
				
				hard['name'] = item['hardware']
				hard['type'] = 1
				hard['depth'] = 1
				hard['size'] = 1
				hard['part_no']= 1234568
				#print hard
				r = self.post_data(hard,'hardwares/')
			if item['building'] not in build:
				build_dic['name']=item['building']
				response = self.post_data(build_dic,'buildings/')

			if item['room'] not in room:
					
				room_dic['name']=item['room']
				response = self.post_data(room_dic,'rooms/')
			if item['rack'] not in rack:
					
				rack_dic['name']=item['rack']
				rack_dic['size']='42'
				rack_dic['room']=item['room']
				response = self.post_data(rack_dic,'racks/')

			if item['name'] not in devices:
					
				response = self.post_data(item,'devices/')
			rack_dic={}
			rack_dic['device'] = item['name']
			rack_dic['rack'] = item['rack']
			rack_dic['room']= item['room']
			rack_dic['start_at'] = 'auto'

			response = self.post_data(rack_dic,'device/rack/')
				#print rack_dic
				#print response
		

		return response
			

	def get_devices(self):
		r = requests.get(url+'devices', auth=(D42_USERNAME, D42_PASSWORD), verify=False)
		#data = json.dumps(r.json())
		resp = json.loads(r.text)
		p = resp['Devices']
			
		if any(i['name']=='sindhoor' for i in p):
			a = next((i for i in p if i['name']=="sindhoor"),False)
			c = json.dumps(a)
			#print a
			return a
	#get_devices()

	def get_data(self,entity):
		
		try:
			r = requests.get(url+entity, auth=(D42_USERNAME, D42_PASSWORD), verify=False)
			data = r.json()
			#print ' %s JSON DATA' %entity.upper()
			#print
			return data

		except Exception:
			print 'Not a valid entity for get_data'

	def post_data(self,data,entity):

		#print 'POSTING %s' %entity[:-1].upper()

		#print (data)
		post_url = url+entity
		#print post_url
		headers = {
				'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD),
				'Content-Type' : 'application/x-www-form-urlencoded'
			}
		try:
			response = requests.post(post_url, data=data, auth=(D42_USERNAME, D42_PASSWORD),\
								  headers=headers, verify=False)
			msg = 'Status code: %s' % str(response)
			#logging.info(msg)
			msg = str(response.text)
		#logger.writer(msg)
			response = response.status_code
			#print 'posted %s' %entity
			return response

		except Exception as e:
			print e
	def post_data_xx(self,D42_URL,params):
	    theurl = D42_URL + "devices/"
	    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain',\
	    			'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD)}
	#    import pdb
	#    pdb.set_trace()
	#    for i in range(0,1):
	#        print json.dumps(data_s[i])
	#        print dict(data_s[i])
	    data = json.dumps(params)
	#    print data
	    resp = requests.post(theurl,auth=(D42_USERNAME,D42_PASSWORD),verify = False,headers=headers,data = data)
	    print resp.text
	    print resp.raise_for_status()
	def delete(self,data,entity):
		#print data,entity
		del_url = 'https://10.0.0.19/api/1.0/'+entity
		headers = {
				'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD),
				'Content-Type' : 'application/x-www-form-urlencoded'
			}
		try:
			response = requests.delete(del_url+data+'/', auth=(D42_USERNAME, D42_PASSWORD),\
								  headers=headers, verify=False)

			response = response.status_code
			return response
			#print 'posted %s' %entity
			#print response
		except Exception as e:
			print e

	def put_data(self,data,entity):
		url = 'https://10.0.0.19/api/1.0/'+entity
		headers = {
				'Authorization' : 'Basic '+ base64.b64encode(D42_USERNAME + ':' + D42_PASSWORD),
				'Content-Type' : 'application/x-www-form-urlencoded'
			}
		try:
			response = requests.put(url,data=data, auth=(D42_USERNAME, D42_PASSWORD),\
								  headers=headers, verify=False)

			response = response.status_code
			return response
			#print 'posted %s' %entity
			#print response
		except Exception as e:
			print e

if __name__ == "__main__":
	device42 = restfull()
	data=[{"aliases": [],
			"asset_no": "",
			"building": "northpark",
			"hardware": "Hardware_1",
			"in_service": "yes",
			"name": "Manmohan",
			}]
	rackdata = [{'device':'Manmohan','rack':'Rack_1','start_at':'auto'}]
	#device=nh-switch-01&building=New Haven DC&room=1st floor&rack=RA1&start_at=2&orientation=back"
	#device42.get_json()
	#device42.data_caching(rackdata,'device/rack/')
	#device42.look_files()
	#device42.email('this is not file')
	#device42.csv_validator('data.csv')
	#device42.parse_arg()
	
	device42.post_data_xx()
	#print time taken to execute

	print datetime.now()-start
