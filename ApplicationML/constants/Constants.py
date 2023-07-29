from enum import Enum

class Constants(Enum):
	FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
	DATEFORMAT= '%Y/%m/%d %H:%M:%S'
	CONFIG_MANDATORY_ATTRIBUTES = ['csv_file', 'epochs', 'batch_size', 'daemon_time']
	CONFIG_ATTRIBUTES_TYPES = {'csv_file': str, 'epochs': int, 'batch_size': int, 'daemon_time': int}
