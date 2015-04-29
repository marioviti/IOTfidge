import sys
import json
import string
from datetime import datetime

#datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
	infile = sys.stdin
	lines = []
	while True:
		line = infile.readline()
		if line == '': break
		lines.append(line.strip())
		line = ''.join(lines)
		line = string.replace(line, '\'', '\"')
		jsonData = json.loads(line)
		if 'daily' in jsonData:
			for entry in jsonData['daily']:
				if 'update_item' in entry:
					if int(entry['update_item']) == 30:
						time = datetime.strptime(entry['time'], '%H:%M:%S.%f')
						print str(time.microsecond)
		if 'item' in jsonData:
			print jsonData['item']
		lines = []
	#el = "{'daily':'3'}"
	#el = string.replace(el, '\'', '\"')
	#jsonData = json.loads(el)
	#print jsonData