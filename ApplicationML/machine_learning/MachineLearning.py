import os
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from OnnxRunner import OnnxRunner


class MachineLearning:
	
	def __init__(self, csv_file, epochs, batch_size, sequence_length, log):
		self.csv_file = csv_file
		self.epochs = epochs
		self.batch_size = batch_size
		self.log = log
		self.model = None
		self.data = pd.read_csv(self.csv_file)
		self.mean_debit = None
		self.std_debit = None
		self.sequence_length = sequence_length
		self.model = None
		self.output_names = None
		self.output_path = "MachineLearningModel.onnx"

	def utc_to_unix(self, utc_timestamp):
		utc_datetime = datetime.strptime(utc_timestamp, "%d.%m.%Y %H:%M:%S")
		return int(utc_datetime.timestamp())

	def train_model(self):
		self.log.info("Training model...")

		self.data['ts'] = self.data['ts'].apply(lambda x: self.utc_to_unix(x))

		self.data = self.data.sort_values(by='ts')

		self.mean_debit = self.data['Flow'].mean()
		self.std_debit = self.data['Flow'].std()
		self.data['normalized_Flow'] = (self.data['Flow'] - self.mean_debit) / self.std_debit

		sequences = []
		targets = []
		for i in range(len(self.data) - self.sequence_length):
		    sequence = self.data['normalized_Flow'].values[i:i + self.sequence_length]
		    target = self.data['normalized_Flow'].values[i + self.sequence_length]
		    sequences.append(sequence)
		    targets.append(target)

		sequences = np.array(sequences)
		targets = np.array(targets)

		x_train, x_test, y_train, y_test = train_test_split(sequences, targets, test_size=0.2)

		self.model = tf.keras.Sequential([
		    tf.keras.layers.LSTM(64, input_shape=(self.sequence_length, 1), activation='tanh', recurrent_activation='sigmoid'),
		    tf.keras.layers.Dense(32, activation='relu'),
		    tf.keras.layers.Dense(16, activation='tanh'),
		    tf.keras.layers.Dense(8, activation='sigmoid'),
		    tf.keras.layers.Dense(1)
		])

		optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
		self.model.compile(optimizer=optimizer, loss='mean_squared_error')

		self.model.fit(x_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=0.1)

		self.log.info("Model is trained")

		mse = self.model.evaluate(x_test, y_test)
		self.log.info("Test Mean Squared Error: {0}".format(mse))

		return

	def model_predict(self, data_stamp):

		unix_timestamp_to_predict = int(data_stamp.timestamp())
		input_sequence = self.data[self.data['ts'] < unix_timestamp_to_predict].tail(self.sequence_length)
		input_sequence = input_sequence['normalized_Flow'].values.reshape(1, -1, 1)

		predicted_normalized_debit = self.model.predict(input_sequence)[0][0]
		predicted_debit = predicted_normalized_debit * self.std_debit + self.mean_debit

		self.log.info("Predicted Debit at {0}: {1:.2f}".format(data_stamp, predicted_debit))

		self.model.save(os.path.join(os.getcwd(), "MachineLearningModel"))

		return

		# l/min
		# compresor car scoate 12 bari si debit de 50 l pe minut -> ce consum are un astfel de compresor -> cost