from enum import Enum

class Constants(Enum):
	FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
	DATEFORMAT= '%d/%m/%Y %H:%M:%S'
	CONFIG_MANDATORY_ATTRIBUTES = ['csv_file', 'daemon_time']
	CONFIG_ATTRIBUTES_TYPES = {'csv_file': str, 'daemon_time': int}
