#!/bin/bash
# Eecution script for the server app

# This initialises the database:
sqlite3 iotfridge.db < iotfridge.sql

#python iotfridge_route.py test.db 2>> log
python iotfridge_route.py iotfridge.db