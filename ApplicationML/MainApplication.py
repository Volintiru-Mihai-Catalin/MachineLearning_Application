from __future__ import absolute_import, division, print_function, unicode_literals

from constants.Constants import Constants
from helpers.Logger import Logger
from helpers.Parsers import ArgsParser, DataParser
from helpers.Validator import Validator
from helpers.CsvReader import CsvReader
from machine_learning.MachineLearning import MachineLearning

import time
from datetime import datetime, timedelta


class MainApplication:

	def __init__(self, args, log, validator):
		self.args = args
		self.log = log
		self.validator = validator
		self.config_data = None
		self.training_df = None
		self.testing_df = None
		self.ml_instance = None

	def execute(self):
		

		try:
			self.log.info("Program has started!")
			self.validator.validate()
			self.config_data = DataParser.parse_json(self.args.config)
			self.ml_instance = MachineLearning(self.config_data['csv_file'], self.log)
			
			while(True):
				self.ml_instance.train_model(datetime.utcnow() + timedelta(days=1))
				time.sleep(self.config_data['daemon_time'])


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