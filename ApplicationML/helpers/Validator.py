from constants.Constants import Constants

import os 
import json

class Validator:
	def __init__(self, config_path, logfile_path):
		self.config_path = config_path
		self.logfile_path = logfile_path
		self.string_err = None

	def check_path_exists(self):
		if not os.path.exists(self.config_path):
			self.err_string = "Config file does not exist!"
		if not os.path.exists(self.logfile_path):
			self.err_string = "Log file does not exist!"

		return

	def check_config_file(self):
		data = None

		if os.stat(self.config_path).st_size == 0:
			self.string_err = "Config file is empty"

		with open(self.config_path, "r") as file:
			data = json.load(file)

		for attribute in Constants.CONFIG_MANDATORY_ATTRIBUTES.value:
			if attribute not in data:
				self.string_err = 'Attribute "{0}" is missing from the configuration file!'.format(attribute)
				break
			if not data[attribute]:
				self.string_err = 'Attribure "{0}" cannot be empty'.format(attribute)
				break

			if type(data[attribute]) is not Constants.CONFIG_ATTRIBUTES_TYPES.value[attribute]:
				self.string_err = 'Attribute "{0}" has type {1}, but the real type should be {2}'.format(attribute, type(data[attribute]).__name__, Constants.CONFIG_ATTRIBUTES_TYPES.value[attribute].__name__)
				break

		return

	def validate(self):
		
		self.check_path_exists()

		if self.string_err:
			raise Exception(self.string_err)

		self.check_config_file()
		
		if self.string_err:
			raise Exception(self.string_err)

		return self.string_err
