import pickle

class OutputHelper:
	def __init__(self, config_path, std_debit, mean_debit, output_names, output_path):
		self.config_path = config_path
		self.std_debit = std_debit
		self.mean_debit = mean_debit
		self.output_names = output_names
		self.output_path = output_path

	def output_formater(self, filename):
		with open(filename, 'wb') as file:
			pickle.dump(self, file)
