#!/bin/bash
# Escution script for the test server app

python tester.py >logtest
python plotter.py <logtest