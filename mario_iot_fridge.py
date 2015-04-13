#!/usr/bin/env python
#shebang!

# Libraries that we need
import sys
import sqlite3 as sql
import json

#define a class for the fridge

class mario_iot_fridge:

	#constructor
	def __init__(self,database_path,inputfile,outputfile)
		self.db = sql.connect(database_path)
		self.cursor = self.db.cursor
		self.infile= inputfile #save the in and out fd
		self.outputfile=outputfile
