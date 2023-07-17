from __future__ import absolute_import, division, print_function, unicode_literals

from constants.Constants import Constants
from helpers.Logger import Logger
from helpers.ArgsParser import ArgsParser

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output
from six.moves import urllib

import tensorflow.compat.v2.feature_column as fc 
import tensorflow as tf


class MainApplication:

	def __init__(self, args, log):
		self.args = args
		self.log = log
		self.err_string = None

	def execute():
		try:
		
			args = parse_arguments()	

			app_log = setup_logging(args.logfile)
			app_log.info("Program has started!")
		
			self.err_string = check_path_exists(args.config, args.logfile)

			if self.err_string:
				raise Exception(self.err_string)

			self.err_string = check_config_file(args.config)
		
			if self.err_string:
				raise Exception(self.err_string)

			doc_train, doc_eval = read_input_data()

		except Exception as e:
			app_log.error(e)

		finally:
			app_log.info("Program has ended!")

def check_path_exists(config_path, logfile_path):
	err_string = None
	if not os.path.exists(config_path):
		err_string = "Config file does not exist!"
	if not os.path.exists(logfile_path):
		err_string = "Log file does not exist!"

	return err_string

def check_config_file(config_path):
	err_string = None
	data = None

	if os.stat(config_path).st_size == 0:
		err_string = "Config file is empty"

	with open(config_path, "r") as file:
		data = json.load(file)

	for attribute in Constants.CONFIG_MANDATORY_ATTRIBUTES.value:
		if attribute not in data:
			err_string = 'Attribute "{0}" is missing from the configuration file!'.format(attribute)
			break
		if not data[attribute]:
			err_string = 'Attribure "{0}" cannot be empty'.format(attribute)
			break

		if type(data[attribute]) is not Constants.CONFIG_ATTRIBUTES_TYPES.value[attribute]:
			err_string = 'Attribute "{0}" has type {1}, but the real type should be {2}'.format(attribute, type(data[attribute]).__name__, constants.CONFIG_ATTRIBUTES_TYPES.value[attribute].__name__)
			break

	return err_string

def read_input_data():
	doc_train = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv')
	doc_eval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')

	return doc_train, doc_eval

if __name__ == "__main__":
	args = ArgsParser.parse_arguments()
	log = Logger.setup_logging(args.logfile)
	print(log)