import pickle

class OutputHelper:
	def __init__(self, number_of_days, sequence_length, data, std_debit, mean_debit, output_names, output_path):
		self.number_of_days = number_of_days
		self.sequence_length = sequence_length
		self.data = data
		self.std_debit = std_debit
		self.mean_debit = mean_debit
		self.output_names = output_names
		self.output_path = output_path

	def output_formater(self, filename):
		with open(filename, 'wb') as file:
			pickle.dump(self, file)
