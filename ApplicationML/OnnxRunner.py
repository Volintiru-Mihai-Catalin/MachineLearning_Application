import os
import tf2onnx
import numpy as np
import pandas as pd
import tensorflow as tf
import onnxruntime as rt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split


class OnnxRunner:
	def __init__(self):
		pass

	def convert_to_onnx(output_path, model):
		spec = (tf.TensorSpec((None, 30, 1), tf.float32, name="input"),)
		
		model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=output_path)
		output_names = [n.name for n in model_proto.graph.output]
		#self.onnx_runner(datetime.utcnow() + timedelta(days=1))

	def onnx_runner(data_stamp, sequence_length, data, std_debit, mean_debit, output_names, output_path, log):
		providers = ['CPUExecutionProvider']
		m = rt.InferenceSession(output_path, providers=providers)

		unix_timestamp_to_predict = int(data_stamp.timestamp())
		input_sequence = data[data['ts'] < unix_timestamp_to_predict].tail(sequence_length)
		input_sequence = input_sequence['normalized_Flow'].values.reshape(1, -1, 1)

		onnx_pred = m.run(output_names, {"input": input_sequence.astype(np.float32)})

		log.info("The predicted debit is: {0}".format(onnx_pred[0][0][0] * std_debit + mean_debit))
