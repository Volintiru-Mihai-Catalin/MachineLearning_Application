import os
import tf2onnx
import numpy as np
import pandas as pd
import tensorflow as tf
import onnxruntime as rt
from datetime import datetime, timedelta
from helpers.Logger import Logger
from sklearn.model_selection import train_test_split


class OnnxRunner:
	def convert_to_onnx(output_path, model):
		spec = (tf.TensorSpec((None, 30, 1), tf.float32, name="input"),)
		
		model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=output_path)
		output_names = [n.name for n in model_proto.graph.output]

	def onnx_runner(metadata):
		predictions = []
		providers = ['CPUExecutionProvider']
		m = rt.InferenceSession(metadata.output_path, providers=providers)

		input_sequence = metadata.data.tail(metadata.sequence_length)
		input_sequence = input_sequence['normalized_Flow'].values.reshape(1, -1, 1)

		for day_number in range(metadata.number_of_days):
			onnx_pred = m.run(metadata.output_names, {"input": input_sequence.astype(np.float32)})
			predictions.append(onnx_pred[0][0][0] * metadata.std_debit + metadata.mean_debit)
			input_sequence[0, day_number, 0] = onnx_pred[0][0][0]

		print(predictions)
