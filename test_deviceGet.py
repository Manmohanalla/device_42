import unittest
from deviceGet import restfull
import subprocess, platform
import sys


class MyTestCase(unittest.TestCase):



	def test_url(self):
		host ='10.0.0.19'
			# Ping parameters as function of OS
		ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
		args = "ping" + " " + ping_str + " " + host
		need_sh = False if  platform.system().lower()=="windows" else True
			# Ping
		result = subprocess.call(args, shell=need_sh) == 0
		self.assertTrue(r)

	def test_url_ping(self):

		self.assertEqual('https://10.0.0.19/api/1.0/',r.url)    

	def test_post_data(self):

		#print 'passing a simple dictionary'
		data = {'name':'sindhoor'}
		entity = 'devices/'
		response = r.post_data(data,entity)
		
		#self.assertIn(0, response)
		self.assertEqual(200,response)
		#self.assertAlmostEqual((7.0**0.5)**2.0, 7.0)

	
	def test_get_devices(self):
		"""Test a simple request."""
		
		response = r.get_devices()
		#print response['name']
		self.assertEqual(response['name'], 'sindhoor')

	
	def test_det_data(self):

		entity = 'devices/'
		search = 'sindhoor'
		response = r.get_data(entity)
		

		ra = map(lambda name: name['name'], filter(lambda name: name['name'] == search, response[entity[:-1].title()]))
		response = response[entity[:-1].title()]
		response = [name['name'] for name in response if name['name'] == search ]
		self.assertIn('sindhoor',ra)
		self.assertTrue(ra)
		response = response[0]
		self.assertEqual('sindhoor',response)

	def test_cashing(self):
		rackdata = [{'device':'Manmohan','rack':'Rack_1','start_at':'auto'}]
		result = r.data_caching(rackdata,'device/rack/')
		self.assertEqual(rackdata,result)

	def test_load(self):

		result = r.load_json('devices.json')
		if result:
			self.assertTrue(True)

	def test_look(self):
		
if __name__ == '__main__':
	r = restfull()
	unittest.main()

