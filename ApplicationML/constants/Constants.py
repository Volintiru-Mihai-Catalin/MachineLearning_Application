from enum import Enum

class Constants(Enum):
	FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
	DATEFORMAT = '%Y-%m-%d %H:%M:%S %Z'
	CONFIG_MANDATORY_ATTRIBUTES = ['csv_path', 'bucket', 'blob', 'epochs', 'batch_size', "sequence_length", "model_output_name", "metadata_output_name"]
	CONFIG_ATTRIBUTES_TYPES = {'csv_path': str, 'bucket': str, 'blob': str, 'epochs': int, 'batch_size': int, "sequence_length": int, "model_output_name": str, "metadata_output_name": str}
