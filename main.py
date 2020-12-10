import csv
from datetime import datetime
import time
import os
import speedtest
import settings

if not os.path.exists(settings.CSV_DIR):
	os.mkdir(settings.CSV_DIR)
RESULTS_FILE = os.path.join(settings.CSV_DIR, f"speed{datetime.now().strftime('%b%d%H%M')}.csv")
TEST_EVERY = 60 * settings.TEST_EVERY


class SpeedTest(speedtest.Speedtest):
	def test(self):
		self.get_servers(settings.SERVERS_LIST)
		self.upload()
		self.download()
		results_dict = self.results.dict()
		download = round(results_dict['download'] / (1024 ** 2), 2)
		upload = round(results_dict['upload'] / (1024 ** 2), 2)
		return download, upload, results_dict['ping']


s = SpeedTest()

with open(RESULTS_FILE, 'w', newline='') as csv_file:
	writer = csv.DictWriter(csv_file, fieldnames=['download', 'upload', 'ping', 'time'])
	writer.writeheader()

prev_test = None

while True:
	if prev_test and not ((since_last_test := time.time() - prev_test) > TEST_EVERY):
		print(f"Next test in {round((TEST_EVERY - since_last_test) / 60)} minutes")
		time.sleep(60)
		continue

	download, upload, ping = s.test()

	with open(RESULTS_FILE, 'a', newline='') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=['download', 'upload', 'ping', 'time'])
		writer.writerow({'download': download,
						 'upload': upload,
						 'ping': ping,
						 'time': datetime.now()})
	prev_test = time.time()
	print(f"Download: {download} | Upload: {upload} | Ping: {ping}")
