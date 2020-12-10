import json

with open('config.json') as file:
	config = json.load(file)

SERVERS_LIST = config["servers"]
GRAPHS_DIR = config["graphs_dir"]
CSV_DIR = config["csv_dir"]
TEST_EVERY = config["test_every"]
