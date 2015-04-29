from exel_reader import exel_reader

import pycurl
from StringIO import StringIO

buffer = StringIO()
c = pycurl.Curl()

import pprint
pp = pprint.PrettyPrinter(indent=4)

from datetime import datetime, timedelta

import sys
import random

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

def open_door():
	return "http://localhost:8080/open_door"

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

def generate_random_expdate():
	num = random.randint(1, 25)
	year = 2015+num%3
	month = 1+num%12
	day = num
	date = str(year)+"-"+str(month)+"-"+str(day)
	return date

def daily_activity(list):
	ret = { }
	i=0
	j=0
	timeList = []
	lenList = len(list)
	if lenList > 30:
		lenList = 30
	sublist = []
	while i < lenList:
		while j<10 and i+j<lenList:
			sublist.append(list[i+j])
			j=j+1
		i=i+j
		j=0
		print "ROUND"
		pp.pprint( send_request(open_door()) )
		insert_item_list(sublist)
		time = datetime.now()
		pp.pprint( send_request(close_door()) )
		dtime =  datetime.now() - time
		print { 'insert_item':str(i),'time':str(dtime) }
		timeList.append({ 'insert_item':str(i),'time':str(dtime) })
		pp.pprint( send_request(open_door()) )
		insert_item_list(sublist)
		sublist = []
		time = datetime.now()
		pp.pprint( send_request(close_door()) )
		dtime =  datetime.now() - time
		print { 'update_item':str(i),'time':str(dtime) }
		timeList.append({ 'update_item':str(i),'time':str(dtime) })
	return { 'daily': timeList }

def insert_list_in_daily(list):
	lim = 30
	lenList = len(list)
	times = len(list)//lim
	for i in range(0,times):
		pre_sublist = list[:lim]
		post_sublist = list[lim:]
		list = post_sublist
		print >> sys.stderr,daily_activity(pre_sublist)

def insert_item_list(list):
	for el in list:
		pp.pprint( send_request(insert_item(el,"","",generate_random_expdate())) )

def remove_item_list(list,expdate):
	for el in list:
		pp.pprint( send_request(remove_item(el,"",expdate)) )

def remove_persist_item_list(list,expdate):
	for el in list:
		pp.pprint( send_request(remove_persist_item(el,"",expdate)) )

if __name__ == '__main__':

	e_reader = exel_reader('docs/Cheese.xlsx')
	#UPClist = e_reader.getUPC()
	#insert_list_in_daily(UPClist)
	#e_reader.new_doc('docs/Fresh-Vegetables.xlsx')
	#UPClist = e_reader.getUPC()
	#insert_list_in_daily(UPClist)
	#e_reader.new_doc('docs/Milk-and-Soy.xlsx')
	#UPClist = e_reader.getUPC()
	#insert_list_in_daily(UPClist)
	#e_reader.new_doc('docs/SingleStrengthJuice1.xlsx')
	#UPClist = e_reader.getUPC()
	#insert_list_in_daily(UPClist)
	e_reader.new_doc('docs/WholeGrains.xlsx')
	UPClist = e_reader.getUPC()
	insert_list_in_daily(UPClist)



