#!/bin/bash
# Example test script for the template that you are given

# This initialises the database:
sqlite3 test.db < test.sql

python iotfridge.py test.db < test.json
