import os
import csv
from google.cloud import storage


class DataBase:
	
	def __init__(self, credentials):
		self.credentials = credentials
		self.client = None
		self.bucket = None
		self.blob = None

	def download_csv(self, path, bucket_name, blob_name):
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials
		self.client = storage.Client()
		self.bucket = self.client.get_bucket(bucket_name)
		self.blob = self.bucket.get_blob(blob_name)

		if self.blob is not None:
			if not os.path.exists(path):
				os.makedirs(path)

			training_csv = os.path.join(path, 'training_data.csv')

			self.blob.download_to_filename(training_csv)


		return training_csv