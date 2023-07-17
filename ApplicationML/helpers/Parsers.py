import json
import argparse


class ArgsParser:
	def __init__(self):
		pass

	def parse_arguments():
		parser = argparse.ArgumentParser()
	
		parser.add_argument('--config', '-c', dest='config', default=None, help='Provide the configuration file (default: None)', required=True)
		parser.add_argument('--log-file', '-l', dest='logfile', default=None, help='Provide the logging file (default: None)', required=True)

		args = parser.parse_args()

		return args

class DataParser:
	def __init__(self):
		pass 

	def parse_json(json_file):
		with open(json_file) as file:
			data = json.load(file)

		return data