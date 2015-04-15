#!/usr/bin/env python
"""
    iotfridge.py - An IoT fridge API

    This software acts as the API between an SQLite database
    and the interfaces to the fridge.

    Remember to initialise a database first!
"""

from outpan import OutpanApi
my_api_key='0004d931710b2493c2497fb10e19a146'
api = OutpanApi(my_api_key)

# Libraries that we need
import sys
import sqlite3 as sql
import json

class IoTFridge:
    """
        Implements the IoT Fridge API
    """

    def __init__(self, dbpath, infile, outfile):
        self.db = sql.connect(dbpath)
        self.cur = self.db.cursor()
        self.infile = infile
        self.outfile = outfile
        self.unique_id = 0

    # Begin API requests

    def req_list(self, reqj):
        resp = { 'response': [], 'success': True }
        for row in self.cur.execute("SELECT * FROM item"):
            # Each row only contains one thing right now, name...
            resp['response'].append({'data': row })
        print >> self.outfile, json.dumps(resp, indent = 1)

    def req_insert(self, reqj):
        data = (self.unique_id, reqj['EAN13'] ,reqj['data']['name'], reqj['data']['expdate'])
        self.unique_id=self.unique_id+1
        self.cur.execute("INSERT INTO item VALUES ( ?, ?, ?, datetime('now','localtime'), ?)", data)
        self.db.commit()
        resp = {'response': 'OK', 'success': True}
        print >> self.outfile, json.dumps(resp)

    # End API requests

    def processRequest(self, req):
        """
            Takes a JSON request, does some simple checking, and tries to call
            the appropriate method to handle the request. The called method is
            responsible for any output.
        """
        jsonData = json.loads(req)
        if "request" in jsonData:
            reqstr = 'req_{0}'.format(jsonData['request'])
            # Echo the request for easier output debugging
            print req
            if reqstr in dir(self):
                getattr(self,reqstr)(jsonData)
            else:
                print >> sys.stderr, "ERROR: {0} not implemented".format(
                    jsonData['request'])
                errorResp = {
                        'response': "{0} not implemented".format(
                            jsonData['request']),
                        'success': False}
                print >> self.outfile, json.dumps(errorResp)
        else:
                print >> sys.stderr, "ERROR: No request attribute in JSON"

    def run(self):
        """
            Read data input, assume a blank line signifies that the buffered
            data should now be parsed as JSON and acted upon
        """
        lines = []
        while True:
            line = self.infile.readline()
            if line == '': break
            lines.append(line.strip())
            if len(lines) > 1 and lines[-1] == '':
                self.processRequest( ''.join(lines) )
                lines = []


if __name__ == '__main__':
    """
        Connect stdin and stdout to accept and emit JSON data

        Non-API content is printed to stderr, so it can be redirected
        independently.
    """
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: python iotfridge.py dbfilename"
        sys.exit(1)
    print >> sys.stderr, "Starting IoTFridge..."
    IOTF = IoTFridge(sys.argv[1], sys.stdin, sys.stdout)
    print >> sys.stderr, "Ready."
    try:
        IOTF.run()
    except KeyboardInterrupt:
        print >> sys.stderr, "Received interrupt, quitting..."
    print >> sys.stderr, "Done"

    # outpan test
    print api.get_product("0072830005555")
