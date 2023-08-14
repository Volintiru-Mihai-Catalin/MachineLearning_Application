import os
from google.cloud import storage
from google.cloud import bigquery
from constants.Constants import Constants


class DataBase:
	
	def __init__(self, credentials, csv_path, project_id, dataset_id, table_id, sequence_length):
		self.credentials = credentials
		self.client = bigquery.Client.from_service_account_json(self.credentials)
		self.csv_path = csv_path
		self.project_id = project_id
		self.dataset_id = dataset_id
		self.table_id = table_id
		self.sequence_length = sequence_length

	def read_from_bigquery(self):
		training_csv = None
		table_ref = f'{self.project_id}.{self.dataset_id}.{self.table_id}'

		query = f'SELECT * FROM `{table_ref}`'

		query_job = self.client.query(query)

		query_job.result()

		if query_job is not None:
			if not os.path.exists(self.csv_path):
				os.makedirs(self.csv_path)

			training_csv = os.path.join(self.csv_path, 'training_data.csv')

			df = query_job.to_dataframe()
			df.to_csv(training_csv, index=False)

		return training_csv

	def create_input_sequence(self):
		input_csv = None
		table_ref = f'{self.project_id}.{self.dataset_id}.{self.table_id}'

		query = f'SELECT * FROM `{table_ref}`'

		query_job = self.client.query(query)

		query_job.result()

		if query_job is not None:
			if not os.path.exists(self.csv_path):
				os.makedirs(self.csv_path)

			input_csv = os.path.join(self.csv_path, 'input_data.csv')

			df = query_job.to_dataframe()
			df.tail(self.sequence_length).to_csv(input_csv, index=False)

		return input_csv
