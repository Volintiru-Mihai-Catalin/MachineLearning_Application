import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from datetime import datetime


class MachineLearning:
	
	def __init__(self, csv_file, log):
		self.csv_file = csv_file
		self.log = log
		self.model = None
		self.a = None 
		self.b = None

	def utc_to_unix(self, utc_timestamp):
		utc_datetime = datetime.strptime(utc_timestamp, "%d.%m.%Y %H:%M:%S")
		return int(utc_datetime.timestamp())

	def train_model(self, data_stamp):
		self.log.info("Training model...")

		data = pd.read_csv(self.csv_file)

		data['ts'] = data['ts'].apply(lambda x: self.utc_to_unix(x))

		# Sort the data by timestamp (if not already sorted)
		data = data.sort_values(by='ts')

		# Normalize the 'debit' data
		mean_debit = data['Flow'].mean()
		std_debit = data['Flow'].std()
		data['normalized_Flow'] = (data['Flow'] - mean_debit) / std_debit

		# Create sequences and targets for the LSTM model
		sequence_length = 30  # Adjust this based on the number of past timestamps you want to consider
		sequences = []
		targets = []
		for i in range(len(data) - sequence_length):
		    sequence = data['normalized_Flow'].values[i:i + sequence_length]
		    target = data['normalized_Flow'].values[i + sequence_length]
		    sequences.append(sequence)
		    targets.append(target)

		sequences = np.array(sequences)
		targets = np.array(targets)

		# Split the data into training and testing sets
		x_train, x_test, y_train, y_test = train_test_split(sequences, targets, test_size=0.2)

		# Create the LSTM model using TensorFlow's Keras API
		model = tf.keras.Sequential([
		    tf.keras.layers.LSTM(64, input_shape=(sequence_length, 1), activation='tanh', recurrent_activation='sigmoid'),
		    tf.keras.layers.Dense(32, activation='relu'),
		    tf.keras.layers.Dense(16, activation='tanh'),
		    tf.keras.layers.Dense(8, activation='sigmoid'),
		    tf.keras.layers.Dense(1)
		])

		# Compile the model
		optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
		model.compile(optimizer=optimizer, loss='mean_squared_error')

		self.log.info("Model is trained")

		# Train the model
		epochs = 500
		batch_size = 8
		model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)

		# Evaluate the model on the test set
		mse = model.evaluate(x_test, y_test)
		print(f"Test Mean Squared Error: {mse}")

		# Make predictions for a given Unix timestamp
		# Replace unix_timestamp_to_predict with your target Unix timestamp (in seconds)
		unix_timestamp_to_predict = int(data_stamp.timestamp())
		input_sequence = data[data['ts'] < unix_timestamp_to_predict].tail(sequence_length)
		input_sequence = input_sequence['normalized_Flow'].values.reshape(1, -1, 1)

		predicted_normalized_debit = model.predict(input_sequence)[0][0]
		predicted_debit = predicted_normalized_debit * std_debit + mean_debit

		print(f"Predicted Debit at {unix_timestamp_to_predict}: {predicted_debit}")
		

		return