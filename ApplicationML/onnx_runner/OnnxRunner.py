import tf2onnx
import numpy as np
import pandas as pd
import tensorflow as tf
import onnxruntime as rt
from database.DataBase import DataBase


class OnnxRunner:
	def convert_to_onnx(output_path, model, sequence_length):
		spec = (tf.TensorSpec((None, sequence_length, 1), tf.float32, name="input"),)
		
		model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=output_path)
		output_names = [n.name for n in model_proto.graph.output]

	def onnx_runner(metadata, config_data):
		predictions = []
		providers = ['CPUExecutionProvider']
		m = rt.InferenceSession(metadata.output_path, providers=providers)

		database = DataBase(config_data['credentials'], config_data['csv_path'], 
			config_data['project_id'], config_data['dataset_id'], config_data['table_id'],
			config_data['sequence_length'])

		data = pd.read_csv(database.create_input_sequence())
		data['normalized_Flow'] = (data['Flow'] - metadata.mean_debit) / metadata.std_debit
		input_sequence = data['normalized_Flow'].values.reshape(1, -1, 1)

		for day_number in range(config_data['number_of_days']):
			onnx_pred = m.run(metadata.output_names, {"input": input_sequence.astype(np.float32)})
			predictions.append(onnx_pred[0][0][0] * metadata.std_debit + metadata.mean_debit)
			list_sequence = input_sequence[0, :, 0].tolist()
			list_sequence.append(onnx_pred[0][0][0])
			list_sequence.pop(0)
			input_sequence = np.array(list_sequence).reshape(1, -1, 1)

		print(predictions)
