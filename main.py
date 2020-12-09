import csv
from datetime import datetime
import time

import speedtest

RESULTS_FILE = f"results/speed{datetime.now().strftime('%b%d%H%M')}.csv"
TEST_EVERY = 60 * 15

s = speedtest.Speedtest()

with open(RESULTS_FILE, 'w', newline='') as csv_file:
	writer = csv.DictWriter(csv_file, fieldnames=['download', 'upload', 'time'])
	writer.writeheader()

prev_test = None

while True:
	if prev_test and not ((since_last_test := time.time() - prev_test) > TEST_EVERY):
		print(f"Next test in {round((TEST_EVERY - since_last_test) / 60)} minutes")
		time.sleep(60)
		continue
	s.get_servers([3402])
	s.upload(threads=None)
	s.download(threads=None)
	s.results.share()
	results_dict = s.results.dict()
	# results_dict = {'download': 10_000_000, 'upload': 5_000_000}

	download, upload = results_dict['download'], results_dict['upload']
	download = round(download / (1024 ** 2), 2)
	upload = round(upload / (1024 ** 2), 2)

	with open(RESULTS_FILE, 'a', newline='') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=['download', 'upload', 'time'])
		writer.writerow({'download': download, 'upload': upload, 'time': datetime.now()})

	prev_test = time.time()
	print(f"Download: {download} | Upload: {upload}")
