import sys
import json
import string
from datetime import datetime
import matplotlib.pyplot as plot

#datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
	infile = sys.stdin
	lines = []
	item = []
	times = []
	it = 0
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
						#print int(time.microsecond)
						item.append(it)
						times.append(int(time.microsecond))
						it = it + 1
		if 'item' in jsonData:
			print jsonData['item']
		lines = []
	plot.title('Daily activity')
	plot.ylabel('microsecond')
	plot.xlabel('30itemUpdate')
	print item
	print times
	plot.bar(item, times, width=1, align="center")
	plot.show()