#routing 
from bottle import route, run, template, response, request, server_names, ServerAdapter
response.content_type = 'application/json'

#misc
from json import dumps
import sys
import collections
check_req_formatting = lambda x, y: collections.Counter(x) == collections.Counter(y)

#dbhandler 
import iotfridgeAPI
db = sys.argv[1]
IOTF = iotfridgeAPI.iotfridgeAPI(db)

# Due to a problem in Installing pyOpenSSL the HTTPS server is disables
#class MySSLCherryPy(ServerAdapter):  
#	def run(self, handler):  
#		from cherrypy import wsgiserver
#		server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler) 
#        # If cert variable is has a valid path, SSL will be used
#        # You can set it to None to disable SSL  
#		cert = 'server.pem' # certificate path   
#		server.ssl_certificate = cert 
#		server.ssl_private_key = cert
#		try:  
#			server.start()  
#		finally:  
#			server.stop()  
#   
#server_names['mysslcherrypy'] = MySSLCherryPy 

@route('/create_usr_passwd')
def index():
	req = { "request" : "create_usr_passwd", "usr" : "" , "passwd" : "" }
	query=request.query
	key_set = query.keys()
	template_req_key_set = ("usr","passwd")
	if check_req_formatting(key_set,template_req_key_set):
		for key in template_req_key_set:
				req[key]=query[key]
		ret = IOTF.processRequest(req)
		return dumps(ret)
	else:
		err_res = dumps({'response':'food_contain: bad request formatting', 'use': template_req_key_set})
		return dumps(err_res)

@route('/food_contain')
def index():
	req = { "request" : "food_contain", "allergen" : "" }
	query=request.query
	key_set = query.keys()
	template_req_key_set = ['allergen']
	if check_req_formatting(key_set,template_req_key_set):
		allergen = []
		for item in [ x.strip() for x in request.url.split('&') ]:
			if 'allergen' in item:
				allergen.append([x.strip() for x in item.split('=')][1])
		req['allergen']=allergen
		ret = IOTF.processRequest(req)
		return dumps(ret)
	else:
		err_res = dumps({'response':'food_contain: bad request formatting', 'use': template_req_key_set})
		return dumps(err_res)

@route('/soon_to_expire')
def index():
	req = { "request" : "soon_to_expire" , "before": ""}
	query=request.query
	key_set = query.keys()
	print key_set
	template_req_key_set = ['before']
	if check_req_formatting(key_set,template_req_key_set):
		for key in template_req_key_set:
				req[key]=query[key]
		ret = IOTF.processRequest(req)
		return dumps(ret)
	err_res = dumps({'response':'soon_to_expire: bad request formatting', 'use': template_req_key_set})
	return dumps(err_res)

@route('/open_door_period')
def index():
	req = { "request" : "open_door_period" , "from": "" , "to" : "" }
	query=request.query
	key_set = query.keys()
	template_req_key_set = ('from','to')
	if check_req_formatting(key_set,template_req_key_set):
		for key in template_req_key_set:
				req[key]=query[key]
		ret = IOTF.processRequest(req)
    	return dumps(ret)
	err_res = dumps({'response':'open_door_period: bad request formatting', 'use': template_req_key_set})
	return dumps(err_res)

@route('/open_door')
def index():
	req = { "request" : "open_door" }
	ret = IOTF.processRequest(req)
    	return dumps(ret)

@route('/close_door')
def index():
	req = { "request" : "close_door" }
	ret = IOTF.processRequest(req)
    	return dumps(ret)

@route('/show_allergies_food')
def index():
	req = { "request" : "show_allergies_food" , "usr": "", "passwd": "" }
	query=request.query
	print query
	key_set = query.keys()
	template_req_key_set = ('usr','passwd')
	if check_req_formatting(key_set,template_req_key_set):
		for key in template_req_key_set:
			req[key]=query[key]
		ret = IOTF.processRequest(req)
		return dumps(ret)
	err_res = dumps({'response':'insert: bad request formatting', 'use': template_req_key_set})
	return err_res

@route('/show_allergies_allergen')
def index():
	req = { "request" : "show_allergies_allergen" , "usr": "", "passwd": "" }
	query=request.query
	print query
	key_set = query.keys()
	template_req_key_set = ('usr','passwd')
	if check_req_formatting(key_set,template_req_key_set):
		for key in template_req_key_set:
			req[key]=query[key]
		ret = IOTF.processRequest(req)
		return dumps(ret)
	err_res = dumps({'response':'insert: bad request formatting', 'use': template_req_key_set})
	return err_res

@route('/show_allergies_allergenListItem')
def index():
	req = { "request" : "show_allergies_allergenListItem" , "usr": "", "passwd": "" }
	query=request.query
	print query
	key_set = query.keys()
	template_req_key_set = ('usr','passwd')
	if check_req_formatting(key_set,template_req_key_set):
		for key in template_req_key_set:
			req[key]=query[key]
		ret = IOTF.processRequest(req)
		return dumps(ret)
	err_res = dumps({'response':'insert: bad request formatting', 'use': template_req_key_set})
	return err_res

@route('/insert')
def index():
	req = { "request" : "insert" , "table": "" , "data" : "{}" }
	datajson={}
	query=request.query
	key_set = query.keys()
	if query['table'] == 'item':
		template_req_key_set = ('table','GTIN','name','ingredients','expdate')
		data_req_key_set = ( 'GTIN','name','ingredients','expdate')
		template_req_key_set2 = ('table','GTIN','name','ingredients','expdate','allergen')
		data_req_key_set2 = ( 'GTIN','name','ingredients','expdate','allergen')
		if check_req_formatting(key_set,template_req_key_set):
			for key in data_req_key_set:
				datajson[key]=query[key]
			req['table']=query['table']
			req['data']=datajson
		elif check_req_formatting(key_set,template_req_key_set2):
			allergen = []
			for item in [ x.strip() for x in request.url.split('&') ]:
				if 'allergen' in item:
					allergen.append([x.strip() for x in item.split('=')][1])
			for key in data_req_key_set:
				datajson[key]=query[key]
			req['table']=query['table']
			req['data']=datajson
			req['data']['allergen']=allergen
		else:
			err_res = dumps({'response':'insert: bad request formatting', 'use': template_req_key_set})
			return dumps(err_res)	
	elif query['table'] == 'profile':
		template_req_key_set = ('table','name','last_name','allergen')
		data_req_key_set = ( 'name','last_name','allergen' )
		if check_req_formatting(key_set,template_req_key_set):
			allergen = []
			for item in [ x.strip() for x in request.url.split('&') ]:
				if 'allergen' in item:
					allergen.append([x.strip() for x in item.split('=')][1])
			for key in data_req_key_set:
				datajson[key]=query[key]
			req['table']=query['table']
			req['data']=datajson
			req['data']['allergen']=allergen
		else:
			err_res = dumps({'response':'insert: bad request formatting', 'use': template_req_key_set})
			return dumps(err_res)
	else:
		err_res = dumps({'response':'insert: bad request formatting', 'tables': ['profile','item']})
		return dumps(err_res)
	res={}
	res = IOTF.processRequest(req)
	return dumps(res)

@route('/remove')
def index():
	req={ "request": "remove", "table": "" }
	datajson={}
	query=request.query
	if query['table'] == 'item' or query['table'] == 'persist_item':
		template_req_key_set = ('table','GTIN','name','expdate')
		data_req_key_set = ('GTIN','name','expdate')
		key_set = query.keys()
	elif query['table'] == 'profile':
		template_req_key_set = ('table','name','last_name')
		data_req_key_set = ('name','last_name')
		key_set = query.keys()
	else:
		err_res = dumps({'response':'remove: bad request formatting', 'tables': ['profile']})
		return dumps(err_res)
	if check_req_formatting(key_set,template_req_key_set):
		req['table']=query['table']
		for key in data_req_key_set:
			datajson[key]=query[key]
			req['table']=query['table']
			req['data']=datajson
		print req
		res = IOTF.processRequest(req)
		return dumps(res)
	else:
		err_res = dumps({'response':'remove: bad request formatting', 'use': template_req_key_set})
		return dumps(err_res)

@route('/list')
def index():
	req={ "request": "list", "table": "" }
	query=request.query
	template_req_key_set = ['table']
	key_set = query.keys()
	if check_req_formatting(key_set,template_req_key_set):
		req['table']=query['table']
		res = IOTF.processRequest(req)
		return dumps(res)
	else:
		err_res = dumps({'response':'bad request formatting'})
		print err_res
		return dumps(err_res)

@route('/demon')
def index():
	res = IOTF.processRequest({ "request": "demon" })
	return dumps(res)

# Due to a problem in Installing pyOpenSSL the HTTPS server is disables
#run(host='localhost', port=8080, server='mysslcherrypy')
run(host='localhost', port=8080)
