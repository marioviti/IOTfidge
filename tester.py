import pycurl
from StringIO import StringIO

buffer = StringIO()
c = pycurl.Curl()

import pprint
pp = pprint.PrettyPrinter(indent=4)

from datetime import datetime, timedelta

def insert_item(GTIN,name,ingredients,expdate):
	return "http://localhost:8080/insert?table=item&GTIN="+GTIN+"&name="+name+"&ingredients="+ingredients+"&expdate="+expdate

def remove_item(GTIN,name,expdate):
	return "http://localhost:8080/remove?table=item&GTIN="+GTIN+"&name="+name+"&expdate="+expdate

def remove_persist_item(GTIN,name,expdate):
	return "http://localhost:8080/remove?table=persist_item&GTIN="+GTIN+"&name="+name+"&expdate="+expdate

def list_table(table):
	return "http://localhost:8080/list?table="+table

def close_door():
	return "http://localhost:8080/demon"

def send_request(req):
	c.setopt(c.URL, req)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	body = ""
	info = c.getinfo(pycurl.HTTP_CODE)
	if  info == 200:
		body = buffer.getvalue()
		buffer.truncate(0)
	else:
		body = { "error from request" : info }
		buffer.truncate(0)
	return body

def daily_activity():

	time = datetime.now()
	for x in range(0, 2):
		pp.pprint( send_request(insert_item("076840100477","","","2015-01-02")) )
		pp.pprint( send_request(insert_item("047834060091","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("016000263123","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("728229123477","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("020000197586","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("026200162300","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("835143002433","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("810979001188","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("024321908203","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("053859070663","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("026400405207","","","2015-02-02")) )
		pp.pprint( send_request(insert_item("041303025666","","","2015-02-02")) )	
	pp.pprint( send_request(close_door()) )
	pp.pprint( send_request(list_table("persist_item")) )

	dtime =  datetime.now() - time
	return dtime

if __name__ == '__main__':

	time_list = []
	for x in range(0, 2):
		time_list.append(str(daily_activity()))

	print time_list
