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

#from outpan import OutpanApi
#my_api_key='0004d931710b2493c2497fb10e19a146'
#api = OutpanApi(my_api_key)

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
        self.open_door_flag = False

    def close_door():
        if self.open_door_flag is True:
            self.open_door_flag = False

    def close_door():
        if self.open_door_flag is False:
            self.open_door_flag = True

    def req_show_allergies_allergen(self, reqj):
        resp = { 'response': {'records' : []}, 'success': True }
        query = "SELECT DISTINCT profile.profile_name, profile.profile_last_name, allergen.allergen_name"+" FROM profile JOIN allergenListProfile"+" ON profile.ID = allergenListProfile.profile_ID"+" JOIN allergen ON allergen.ID=allergenListProfile.allergen_ID"
        i = 0
        for row in self.cur.execute(query):
            i = 0
            for entry in row:
                resp['response']['records'].append({self.cur.description[i][0]: entry})
                i = i+1
        self.db.commit()
        return resp

    def req_show_allergies_allergenListItem(self, reqj):
        resp = { 'response': {'records' : []}, 'success': True }
        query = "SELECT DISTINCT persist_item.item_name, allergen.allergen_name"+" FROM persist_item JOIN persist_allergenListItem"+" ON persist_item.ID = persist_allergenListItem.item_ID"+" JOIN allergen ON allergen.ID=persist_allergenListItem.allergen_ID"
        i = 0
        for row in self.cur.execute(query):
            i = 0
            for entry in row:
                resp['response']['records'].append({self.cur.description[i][0]: entry})
                i = i+1
        self.db.commit()
        return resp

    def req_show_allergies_food(self, reqj):
        resp = { 'response': {'records' : []}, 'success': True }
        query = "SELECT DISTINCT persist_item.item_name, profile.profile_name, profile.profile_last_name"+" FROM persist_item JOIN persist_allergenListItem"+" ON persist_item.ID = persist_allergenListItem.item_ID"+" JOIN allergenListProfile ON persist_allergenListItem.allergen_ID=allergenListProfile.allergen_ID"+" JOIN profile ON profile.ID=allergenListProfile.profile_ID"
        i = 0
        for row in self.cur.execute(query):
            i = 0
            for entry in row:
                resp['response']['records'].append({self.cur.description[i][0]: entry})
                i = i+1
        self.db.commit()
        return resp

    def req_list(self, reqj):
        resp = { 'response': { 'table': reqj['table'] , 'records' : []}, 'success': True }
        query = "SELECT * FROM "+ reqj['table']
        i = 0
        for row in self.cur.execute(query):
            i = 0
            for entry in row:
                resp['response']['records'].append({self.cur.description[i][0]: entry})
                i = i+1
        self.db.commit()
        return resp

    def req_remove_persist_item(self, reqj):
        res = { 'response': 'NOT IMPLEMENTED', 'success': True }
        if reqj['data']['GTIN'] is not "NULL":
            data = (reqj['data']['GTIN'],reqj['data']['expdate']) 
            food_id = 0
            qt = 0
            for row in self.cur.execute("SELECT persist_item.ID, persist_item.qt FROM persist_item JOIN itemdate ON persist_item.ID=itemdate.item_ID WHERE GTIN = ? AND expdate = ?",data):
                food_id = row[0]
                qt = row[1]
            res = { 'response': 'NO ROW AFFECTED', 'success': True }
            if qt>0:
                data = [food_id]
                self.cur.execute("UPDATE itemdate SET outdate = datetime('now','localtime') WHERE item_ID=?",data)
                if self.cur.rowcount == 0:
                    self.db.commit()
                    return res
                self.cur.execute("UPDATE persist_item SET qt = qt - 1 WHERE ID=?",data)
                if self.cur.rowcount == 0:
                    self.db.commit()
                    return res
                else:
                    self.db.commit()
                    res = { 'response': 'OK', 'success': True }
                    return res

            else:
                self.db.commit()
                return res
        return res

    def req_remove_item(self, reqj):
        res = { 'response': 'NOT IMPLEMENTED', 'success': True }
        if reqj['data']['GTIN'] is not "NULL":
            data = (reqj['data']['GTIN'],reqj['data']['expdate'])
            self.cur.execute("PRAGMA foreign_keys=ON")
            self.cur.execute("DELETE FROM item WHERE GTIN=? AND expdate=?",data)
            if self.cur.rowcount == 0:
                res = { 'response': 'NO ROW AFFECTED', 'success': True }
            else:
                res = { 'response': 'OK', 'success': True }
            self.db.commit()
        return res

    def req_remove_profile(self, reqj):
        data = (reqj['data']['name'],reqj['data']['last_name'])
        self.cur.execute("PRAGMA foreign_keys=ON")
        self.cur.execute("DELETE FROM profile WHERE profile_name=? AND profile_last_name=?",data)
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
        for rows in self.cur.execute("SELECT DISTINCT GTIN, item_name, ingredients, COUNT(ID), ID FROM item GROUP BY GTIN, item_name, ingredients"):
            data = (rows[0],rows[1],rows[2],rows[3])
            print rows
            updata = (rows[3],rows[0],rows[1],rows[2])
            temp_curr.execute("UPDATE persist_item SET qt = qt + ? WHERE GTIN = ? AND item_name = ? AND ingredients = ?", updata)
            if temp_curr.rowcount == 0:
                temp_curr.execute("INSERT INTO persist_item VALUES(NULL,?,?,?,?)",data)
                food_ID=0
                for row_in in temp_curr.execute("SELECT MAX(ID) FROM persist_item"):
                    food_ID=row_in[0]
                data = (rows[0],rows[1],rows[2])
                for rows_in_in in temp_curr.execute("SELECT indate, expdate FROM item WHERE GTIN = ? AND item_name = ? AND ingredients = ?",data):
                    print rows_in_in
                    data_in_in = (food_ID, rows_in_in[0], rows_in_in[1])
                    temp_curr_2.execute("INSERT INTO itemdate VALUES (NULL, ?, ?, ?, NULL)",data_in_in)
                data=[rows[4]]
                for rows_in_in in temp_curr.execute("SELECT allergen.allergen_name, allergen.ID FROM allergen JOIN allergenListItem ON allergen.ID=allergenListItem.allergen_ID WHERE allergenListItem.item_ID=? ",data):
                    print rows_in_in
                    data_in_in = (food_ID, rows_in_in[1])
                    temp_curr_2.execute("INSERT INTO persist_allergenListItem VALUES (NULL, ?, ?)",data_in_in)
            else:
                food_ID=0
                data = (rows[0],rows[1],rows[2])
                for row_in in temp_curr.execute("SELECT ID FROM persist_item WHERE GTIN = ? AND item_name = ? AND ingredients = ?",data):
                    food_ID=row_in[0]
                for rows_in_in in temp_curr.execute("SELECT indate, expdate FROM item WHERE GTIN = ? AND item_name = ? AND ingredients = ?",data):
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
        """
            reqj has GTIN, name, ingredients, expdate.
            if GTIN is not NULL info will be fetched from the LabelAPI
            else name and ingredients provided will be inserted in the database
        """
        allergens=[]
        GTIN = reqj['data']['GTIN']
        name = ""
        ingredients = ""
        expdate = ""
        if GTIN != 'NULL':
            data = [reqj['data']['GTIN']]
            query_ret = self.cur.execute("SELECT ID, item_name, ingredients FROM item WHERE GTIN = ?", data)
            count=0
            for row in query_ret:
                print row
                data = [row[0]]
                name = row[1]
                ingredients = row[2]
                expdate = reqj['data']['expdate']
                for rec in self.cur.execute("SELECT allergen.allergen_name FROM allergen JOIN allergenListItem ON allergen.ID = allergenListItem.allergen_ID WHERE allergenListItem.item_ID = ?", data):
                    allergens.append({"allergen_value": 2, "allergen_name": rec[0]})
                self.db.commit()
                count = count+1
            if count == 0:
                self.db.commit()
                labeldata = self.api.getdata(reqj['data']['GTIN'])
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
                for row in self.cur.execute("SELECT ID FROM allergen WHERE allergen.allergen_name=?",data):
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
            for row in self.cur.execute("SELECT ID FROM allergen WHERE allergen.allergen_name=?",data):
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
