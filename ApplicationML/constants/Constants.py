from enum import Enum

class Constants(Enum):
	FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
	DATEFORMAT= '%d/%m/%Y %H:%M:%S'
	CONFIG_MANDATORY_ATTRIBUTES = ['training_data', 'evaluating_data', 'daemon_time']
	CONFIG_ATTRIBUTES_TYPES = {'training_data': str, 'evaluating_data': str, 'daemon_time': int}
