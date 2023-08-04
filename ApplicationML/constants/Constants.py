from enum import Enum

class Constants(Enum):
	FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
	DATEFORMAT= '%Y/%m/%d %H:%M:%S'
	CONFIG_MANDATORY_ATTRIBUTES = ['csv_file', 'epochs', 'batch_size', "sequence_length", "output_path"]
	CONFIG_ATTRIBUTES_TYPES = {'csv_file': str, 'epochs': int, 'batch_size': int, "sequence_length": int, "output_path": str}
