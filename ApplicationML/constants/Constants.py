from enum import Enum

class Constants(Enum):
	FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
	DATEFORMAT = '%Y-%m-%d %H:%M:%S%z'
	CONFIG_MANDATORY_ATTRIBUTES = ['csv_path', 'project_id', 'dataset_id', 'table_id', 'epochs', 'batch_size', "sequence_length", "number_of_days", "model_output_name", "metadata_output_name"]
	CONFIG_ATTRIBUTES_TYPES = {'csv_path': str, 'project_id': str, 'dataset_id': str, 'table_id': str, 'epochs': int, 'batch_size': int, "sequence_length": int, "number_of_days": int, "model_output_name": str, "metadata_output_name": str}
