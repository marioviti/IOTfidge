#labelApi

import requests
apikey = '4cy7zxu8hbjfnugdgrnpeekc'

import pprint
pp = pprint.PrettyPrinter(indent=4)

# 'http://api.foodessentials.com/createsession?
#	uid=marioviti.LabelApi&
#	devid=fridge_01&
#	appid=iot_fridge&
#	f=json&
#	api_key=4cy7zxu8hbjfnugdgrnpeekc'


# {
#     "session_id": "a003b12d-dbb5-4fe7-8ec0-3d6e799b0e29",
#     "user_id": "marioviti.LabelApi",
#     "app_id": "iot_fridge",
#     "device_id": "fridge_01",
#     "validUser": "true",
#     "version": "1.01",
#     "retailer_id": 1
# }


# http://api.foodessentials.com/label?
#	u=072830005555&
#	sid=0cd7e9b7-ebe4-4c68-9415-a8f7d1be9ede&
#	appid=demoApp_01&
#	f=json&
#	long=38.6300&lat=90.2000& OPTIONAL
#	api_key=4cy7zxu8hbjfnugdgrnpeekc

class request:

	def __init__(self,user,dev,app,key):
		self.url = 'http://api.foodessentials.com/'
		self.user = user
		self.dev = dev
		self.app = app
		self.key = key
		url = self.url + 'createsession'
		self.params = {'uid': self.user, 'devid': self.dev, 'appid': self.app, 'f':'json', 'api_key': self.key}
		session = requests.get( url, params=self.params )
		self.status = session.status_code
		self.session = session.json()
		self.sessionid =  self.session['session_id']

	def parseupc(self, upc):
		upcbit = upc.split();
		produpc = ''
		for upcs in upcbit:
			produpc = produpc + upcs
		return produpc

	def updateSession(self):
		url = self.url + 'createsession'
		self.params = {'uid': self.user, 'devid': self.dev, 'appid': self.app, 'f':'json', 'api_key': self.key}
		session = requests.get( url, params=self.params )
		self.status = session.status_code
		self.session = session.json()
		self.sessionid =  self.session['session_id']
		return self.status

	def getdata(self, upc):
		produpc = self.parseupc(upc)
		url = self.url + 'label'
		self.params = { 'u': produpc ,'sid': self.sessionid, 'appid': self.app, 'f':'json', 'api_key': self.key }
		label = requests.get( url, params=self.params )
		ret = label.json()
		self.status = label.status_code
		if self.status != 200 : 
			self.updateSession()
			ret = self.getdata(produpc)
		return ret

if __name__ == '__main__':

	fridgeApi = request('marioviti.LabelApi','iot_fridge','fridge_01',apikey)
	pp.pprint(fridgeApi.getdata('072830005555'))

