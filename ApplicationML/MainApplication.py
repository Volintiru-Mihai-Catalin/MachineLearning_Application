from __future__ import absolute_import, division, print_function, unicode_literals

from constants.Constants import Constants
from helpers.Logger import Logger
from helpers.Parsers import ArgsParser, DataParser
from helpers.Validator import Validator
from helpers.CsvReader import CsvReader

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from IPython.display import clear_output
# from six.moves import urllib

# import tensorflow.compat.v2.feature_column as fc 
# import tensorflow as tf


class MainApplication:

	def __init__(self, args, log, validator):
		self.args = args
		self.log = log
		self.validator = validator
		self.config_data = None
		self.training_df = None
		self.testing_df = None

	def execute(self):
		
		try:
			self.log.info("Program has started!")
			self.validator.validate()
			self.config_data = DataParser.parse_json(self.args.config)
			self.training_df, self.testing_df = CsvReader.csv_separator(self.config_data['csv_file'])

		except Exception as e:
			self.log.error(e)

		finally:
			self.log.info("Program has ended!")


if __name__ == "__main__":
	
	args = ArgsParser.parse_arguments()
	log = Logger.setup_logging(args.logfile)
	validator = Validator(args.config, args.logfile)
	app = MainApplication(args, log, validator)
	
	app.execute()