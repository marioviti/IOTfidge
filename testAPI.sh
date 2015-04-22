#!/bin/bash
# Eecution script for the server app

# This initialises the database:
sqlite3 test.db < test.sql

python iotfridge_route.py test.db