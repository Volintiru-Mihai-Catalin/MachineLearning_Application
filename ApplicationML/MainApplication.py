from helpers.Logger import Logger
from helpers.Parsers import ArgsParser, DataParser
from helpers.Validator import Validator
from helpers.CsvReader import CsvReader
from helpers.OutputHelper import OutputHelper
from onnx_runner.OnnxRunner import OnnxRunner
from machine_learning.MachineLearning import MachineLearning
from database.DataBase import DataBase


class MainApplication:

	def __init__(self, args, log, validator):
		self.args = args
		self.log = log
		self.validator = validator
		self.config_data = None
		self.training_df = None
		self.testing_df = None
		self.ml_instance = None
		self.output_instance = None
		self.database = None
		self.training_csv = None

	def execute(self):
		try:
			self.log.info("Program has started!")

			# se valideaza fisierul de configuratie
			self.validator.validate()
			self.config_data = DataParser.parse_json(self.args.config)

			# se initializeaza baza de date
			self.database = DataBase(self.config_data['credentials'], self.config_data['csv_path'],
				self.config_data['project_id'], self.config_data['dataset_id'], 
				self.config_data['table_id'], self.config_data['sequence_length'])
			
			self.training_csv = self.database.read_from_bigquery()
			self.ml_instance = MachineLearning(self.training_csv, 
				self.config_data['epochs'], self.config_data['batch_size'], 
				self.config_data['sequence_length'], self.log)
			
			self.ml_instance.train_model()

			# se salveaza modelul in format ONNX
			OnnxRunner.convert_to_onnx(self.config_data['model_output_name'], self.ml_instance.model,
				self.config_data['sequence_length'])
			self.output_instance = OutputHelper(self.args.config, self.ml_instance.std_debit,
				self.ml_instance.mean_debit, self.ml_instance.output_names, 
				self.ml_instance.output_path)

			# se salveaza output-ul pentru urmatoarea aplicatie
			self.output_instance.output_formater(self.config_data['metadata_output_name'])
			
		except Exception as e:
			self.log.error(e)

		finally:
			self.log.info("Program has ended!")


if __name__ == "__main__":
	
	# parseaza argumentele
	args = ArgsParser.parse_arguments()
	
	log = Logger.setup_logging(args.logfile)
	validator = Validator(args.config, args.logfile)
	app = MainApplication(args, log, validator)
	
	app.execute()