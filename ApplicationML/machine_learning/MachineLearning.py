import numpy as np
from datetime import datetime
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class MachineLearning:
	
	def __init__(self, training_df, testing_df, log):
		self.training_df = training_df
		self.testing_df = testing_df
		self.log = log
		self.model = None
		self.a = None 
		self.b = None

	def utc_to_unix(self, utc_timestamp):
		utc_datetime = datetime.strptime(utc_timestamp, "%d.%m.%Y %H:%M:%S")
		return int(utc_datetime.timestamp())

	def train_model(self):
		self.log.info("Training model...")

		timestamps = np.vectorize(self.utc_to_unix)(self.training_df['ts'].values)
		flow = self.training_df['Flow']

		print(flow)

		mean_flow = np.mean(flow)
		std_flow = np.std(flow)
		flow_normalized = (flow - mean_flow) / std_flow

		self.model = Sequential()
		self.model.add(Dense(64, activation='relu', input_shape=(1,)))
		self.model.add(Dense(32, activation='relu'))
		self.model.add(Dense(1))
		self.model.compile(optimizer='adam', loss='mse')

		self.model.fit(timestamps, flow_normalized, epochs=100, batch_size=32, verbose=1)

		testing_timestamps = np.vectorize(self.utc_to_unix)(self.testing_df['ts'].values)
		testing_flow = self.testing_df['Flow']

		testing_mean_flow = np.mean(testing_flow)
		testing_std_flow = np.std(testing_flow)
		testing_flow_normalized = (testing_flow - testing_mean_flow) / testing_std_flow

		loss = self.model.evaluate(testing_timestamps, testing_flow_normalized)
		print(f'Test Loss: {loss:.4f}')

		self.a = std_flow
		self.b = mean_flow

		self.log.info("Model is trained")

	def predict_value(self, data_stamp):
		if data_stamp <= datetime.utcnow():
			self.log.warning("Can't predict a date from the past!")
			return

		new_timestamp = int(data_stamp.timestamp())
		normalized_debit_prediction = self.model.predict(np.array([new_timestamp]))[0][0]
		predicted_debit = normalized_debit_prediction * self.a + self.b 
		print(f'Predicted Debit at Timestamp {new_timestamp}: {predicted_debit:.2f}')

		return