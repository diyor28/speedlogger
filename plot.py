from datetime import datetime

import matplotlib.pyplot as plt
import csv
import os
import matplotlib.dates as mdates

data = []
for file in os.listdir('results'):
	with open(os.path.join('results', file), 'r') as csv_file:
		reader = csv.DictReader(csv_file)
		for row in reader:
			data.append(row)

data = [{'download': float(el['download']), 'upload': float(el['upload']), 'time': datetime.fromisoformat(el['time'])} for el in data]
data.sort(key=lambda x: x['time'])

download_speeds = [int(el['download']) for el in data]
upload_speeds = [int(el['upload']) for el in data]
time_axis = [el['time'] for el in data]
fig = plt.figure(figsize=(10, 5))
ax = plt.gca()
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)
plt.yticks(list(range(min(download_speeds), max(download_speeds), 2)))
plt.xlabel('Time')
plt.ylabel('Speed')
plt.plot(time_axis, download_speeds)
plt.plot(time_axis, upload_speeds)
plt.legend(['Download', 'Upload'])
plt.show()
fig.savefig('graph.png')
