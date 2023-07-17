from constants.Constants import Constants

import logging

class Logger:

	def __init__(self):
		pass

	def setup_logging(logfile):
		log_formatter = logging.Formatter(Constants.FORMAT.value, datefmt=Constants.DATEFORMAT.value)
	
		file_handler = logging.FileHandler(logfile)
		file_handler.setFormatter(log_formatter)
		file_handler.setLevel(logging.INFO)

		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(log_formatter)
		stream_handler.setLevel(logging.INFO)

		app_log = logging.getLogger('root')
		app_log.setLevel(logging.INFO)

		app_log.addHandler(file_handler)
		app_log.addHandler(stream_handler)

		return app_log