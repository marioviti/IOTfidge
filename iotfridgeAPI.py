#!/usr/bin/env python
"""
    iotfridgeAPI.py - An IoT fridge API

    This software acts as the API between an SQLite database
    and the interfaces to the fridge.

    Remember to initialise a database first!
"""

# Libraries that we need
import sys
import sqlite3 as sql
import json

from outpan import OutpanApi
my_api_key='0004d931710b2493c2497fb10e19a146'
api = OutpanApi(my_api_key)

import pprint
pp = pprint.PrettyPrinter(indent=4)

import labelApi
labelApikey = '4cy7zxu8hbjfnugdgrnpeekc'
user = 'marioviti.LabelApi'
app = 'iot_fridge'
dev = 'fridge_01'

class iotfridgeAPI:
    """
        Implements the IoT Fridge API
    """
    def __init__(self, dbpath):
        self.db = sql.connect(dbpath)
        self.cur = self.db.cursor()
        self.api = labelApi.request(user, app, dev, labelApikey)

    def req_list(self, reqj):
        resp = { 'response': { 'table': reqj['table'] , 'records' : []}, 'success': True }
        query = "SELECT * FROM "+ reqj['table']
        i = 0
        for row in self.cur.execute(query):
            i = 0
            for entry in row:
                resp['response']['records'].append({self.cur.description[i][0]: entry})
                i = i+1
        return resp

    def req_remove_item(self, reqj):
        resp = { 'response':'NOT IMPLEMENTED', 'success': True }
        json.dumps(resp, indent = 1)

    def req_remove_profile(self, reqj):
        data = (reqj['data']['name'],reqj['data']['last_name'])
        self.cur.execute("PRAGMA foreign_keys=ON")
        self.cur.execute("DELETE FROM profile WHERE name=? AND last_name=?",data)
        if self.cur.rowcount == 0:
            res = { 'response': 'NO ROW AFFECTED', 'success': True }
        else:
            res = { 'response': 'OK', 'success': True }
        self.db.commit()
        return res

    def req_remove(self, reqj):
        reqstr = 'req_remove_{0}'.format(reqj['table'])
        if reqstr in dir(self):
            resp = getattr(self,reqstr)(reqj)
        else:
            resp = { 'response': 'req_remove: BAD REQUEST FORMATTING ', 'success': False }
        return resp

    def req_demon(self, reqj):
        # THIS SHOULD NEVER FAIL
        temp_curr=self.db.cursor()
        temp_curr_2=self.db.cursor()
        for rows in self.cur.execute("SELECT DISTINCT GTIN, NAME, ingredients, COUNT(ID), ID FROM item GROUP BY GTIN, NAME, ingredients"):
            data = (rows[0],rows[1],rows[2],rows[3])
            print rows
            updata = (rows[3],rows[0],rows[1],rows[2])
            temp_curr.execute("UPDATE persist_item SET qt = qt + ? WHERE GTIN = ? AND NAME = ? AND ingredients = ?", updata)
            if temp_curr.rowcount == 0:
                temp_curr.execute("INSERT INTO persist_item VALUES(NULL,?,?,?,?)",data)
                food_ID=0
                for row_in in temp_curr.execute("SELECT MAX(ID) FROM persist_item"):
                    food_ID=row_in[0]
                data = (rows[0],rows[1],rows[2])
                for rows_in_in in temp_curr.execute("SELECT indate, expdate FROM item WHERE GTIN = ? AND NAME = ? AND ingredients = ?",data):
                    print rows_in_in
                    data_in_in = (food_ID, rows_in_in[0], rows_in_in[1])
                    temp_curr_2.execute("INSERT INTO itemdate VALUES (NULL, ?, ?, ?, NULL)",data_in_in)
                data=[rows[4]]
                for rows_in_in in temp_curr.execute("SELECT allergen.name, allergen.ID FROM allergen JOIN allergenListItem ON allergen.ID=allergenListItem.allergenID WHERE allergenListItem.foodID=? ",data):
                    print rows_in_in
                    data_in_in = (food_ID, rows_in_in[1])
                    temp_curr_2.execute("INSERT INTO persist_allergenListItem VALUES (NULL, ?, ?)",data_in_in)
            else:
                food_ID=0
                data = (rows[0],rows[1],rows[2])
                for row_in in temp_curr.execute("SELECT ID FROM persist_item WHERE GTIN = ? AND NAME = ? AND ingredients = ?",data):
                    food_ID=row_in[0]
                for rows_in_in in temp_curr.execute("SELECT indate, expdate FROM item WHERE GTIN = ? AND NAME = ? AND ingredients = ?",data):
                    print rows_in_in
                    data_in_in = (food_ID, rows_in_in[0], rows_in_in[1])
                    temp_curr_2.execute("INSERT INTO itemdate VALUES (NULL, ?, ?, ?, NULL)",data_in_in)
        self.db.commit()
        self.cur.execute("PRAGMA foreign_keys=ON")
        self.cur.execute("DELETE FROM item")
        self.db.commit()
        resp = {'response': 'OK', 'success': True}
        return resp

    def req_insert(self,reqj):
        reqstr = 'req_insert_{0}'.format(reqj['table'])
        if reqstr in dir(self):
            return getattr(self,reqstr)(reqj)
        else:
            resp = { 'response': 'req_insert: BAD REQUEST FORMATTING FOR INSERT' , 'success': False }
            return resp

    def req_insert_item(self, reqj):
        print "in insert_item"
        allergens=[]
        if reqj['data']['GTIN'] != 'NULL':
            labeldata = self.api.getdata(reqj['data']['GTIN'])
            GTIN = reqj['data']['GTIN']
            name = labeldata['product_name']
            ingredients = labeldata['ingredients']
            expdate = reqj['data']['expdate']
            allergens = labeldata['allergens']
        else:
            GTIN = reqj['data']['GTIN']
            name = reqj['data']['name']
            ingredients = reqj['data']['ingredients']
            expdate = reqj['data']['expdate']
        data = ( GTIN, name, ingredients, expdate)
        self.cur.execute("INSERT INTO item VALUES ( NULL, ?, ?, ?, datetime('now','localtime'), ?)", data)
        for row in self.cur.execute("SELECT MAX(ID) FROM item"):
            item_id = row[0]
        for allergen in allergens:
            if allergen['allergen_value']!=0:
                allergen_id=0
                data=[allergen['allergen_name'].upper()]
                for row in self.cur.execute("SELECT ID FROM allergen WHERE allergen.name=?",data):
                    allergen_id=row[0]
                if allergen_id!=0:
                    data=(item_id,allergen_id)
                else:
                    self.cur.execute("INSERT INTO allergen VALUES (NULL, ?)", data )
                    for row in self.cur.execute("SELECT MAX(ID) FROM allergen"):
                        allergen_id = row[0]
                    data=(item_id,allergen_id)
                self.cur.execute("INSERT INTO allergenListItem VALUES (NULL,?,?)",data)
        self.db.commit()
        resp = {'response': 'OK', 'success': True}
        return resp

    def req_insert_profile(self, reqj):
        """
            reqj has name, last_name, allergen list.
            name and last_name are insert in profile table,
            allergen list are inserted in allergen table
        """
        data = (reqj['data']['name'], reqj['data']['last_name'])
        self.cur.execute("INSERT INTO profile VALUES (NULL, ?, ?)", data)
        profile_id = 0
        for profile in self.cur.execute("SELECT MAX(ID) FROM profile"):
            profile_id = profile[0]
        for allergen in reqj['data']['allergen']:
            allergen_id = 0
            data = [allergen.upper()]
            for row in self.cur.execute("SELECT ID FROM allergen WHERE allergen.name=?",data):
                allergen_id = row[0]
            if allergen_id == 0:
                self.cur.execute("INSERT INTO allergen VALUES (NULL, ?)", data )
                for row in self.cur.execute("SELECT MAX(ID) FROM allergen"):
                    allergen_id = row[0]
            data = (profile_id,allergen_id)
            self.cur.execute("INSERT INTO allergenListProfile VALUES (NULL, ?,?)", data )
        self.db.commit()
        resp = {'response': 'OK', 'success': True}
        return resp

    def processRequest(self, req):
        """
            Takes a JSON request from the router
        """
        jsonData = req
        if "request" in jsonData:
            reqstr = 'req_{0}'.format(jsonData['request'])
            print >> sys.stderr, reqstr
            # Echo the request for easier output debugging
            print >> sys.stderr, req
            if reqstr in dir(self):
                return getattr(self,reqstr)(jsonData)
            else:
                print >> sys.stderr, "ERROR: {0} not implemented".format(
                    jsonData['request'])
                errorResp = {
                        'response': "{0} not implemented".format(
                            jsonData['request']),
                        'success': False}
                return errorResp
        else:
            print >> sys.stderr, "ERROR: No request attribute in JSON"
            errorResp = {'response': 'no request found' ,'success': False }
            return errorResp
