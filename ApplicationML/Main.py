import pickle
from datetime import datetime, timedelta

from onnx_runner.OnnxRunner import OnnxRunner


if __name__ == "__main__":
	file = "output.pkl"
	with open(file, "rb") as f:
		metadata = pickle.load(f)
	
	OnnxRunner.onnx_runner(metadata) 
