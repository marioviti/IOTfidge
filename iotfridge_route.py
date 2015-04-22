#routing 
from bottle import route, run, template, response, request
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

@route('/hello')
def index():
	req = { "request" : "hello" , "data" : "{}"}
	datajson={}
	data = request.query.iterallitems()
	for val in data:
		datajson[val[0]]=val[1] 
	req['data']=datajson
	print datajson
	ret = IOTF.processRequest(req)
    	return dumps(ret)

#{ "request": "insert", "table": "item" , "data": { "GTIN": "NULL", "name": "Cheese", "ingredients": "MILK", "expdate": "2016-03-12" } }
#{ "request": "insert", "table": "item" , "data":  {"name": "Giulia", "last_name": "Biasci" , "allergen": ["Colors","berry"]} }
@route('/insert')
def index():
	req = { "request" : "insert" , "table": "" , "data" : "{}" }
	datajson={}
	query=request.query
	key_set = query.keys()
	if query['table'] == 'item':
		template_req_key_set = ('table','GTIN','name','ingredients','expdate')
		data_req_key_set = ( 'GTIN','name','ingredients','expdate')
		if check_req_formatting(key_set,template_req_key_set):
			for key in data_req_key_set:
				datajson[key]=query[key]
			req['table']=query['table']
			req['data']=datajson
		else:
			err_res = dumps({'response':'bad request formatting'})
			print err_res
			return dumps(err_res)	
	elif query['table'] == 'profile':
		template_req_key_set = ('table','name','last_name','allergen')
		data_req_key_set = ( 'name','last_name','allergen' )
		if check_req_formatting(key_set,template_req_key_set):
			allergen = [x.strip() for x in query['allergen'].split(',')]
			for key in data_req_key_set:
				datajson[key]=query[key]
			req['table']=query['table']
			req['data']=datajson
			req['data']['allergen']=allergen
		else:
			err_res = dumps({'response':'bad request formatting'})
			print err_res
			return dumps(err_res)
	else:
		err_res = dumps({'response':'bad request formatting'})
		return dumps(err_res)
	res={}
	res = IOTF.processRequest(req)
	return dumps(res)

@route('/remove')
def index():
	req={ "request": "remove", "table": "" }
	datajson={}
	query=request.query
	if query['table'] == 'item':
		print "will do"
		req = {}
	elif  query['table'] == 'profile':
		template_req_key_set = ('table','name','last_name')
		data_req_key_set = ('name','last_name')
		key_set = query.keys()
		if check_req_formatting(key_set,template_req_key_set):
			req['table']=query['table']
			for key in data_req_key_set:
				datajson[key]=query[key]
				req['table']=query['table']
				req['data']=datajson
		res = IOTF.processRequest(req)
		return dumps(res)
	else:
		err_res = dumps({'response':'bad request formatting'})
		print err_res
		return dumps(err_res)
	res = IOTF.processRequest(req)
	return dumps(res)


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


run(host='localhost', port=8080)