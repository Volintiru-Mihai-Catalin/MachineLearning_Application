import pickle
from helpers.Parsers import DataParser

from onnx_runner.OnnxRunner import OnnxRunner


if __name__ == "__main__":
	file = "output.pkl"
	with open(file, "rb") as f:
		metadata = pickle.load(f)

	config_data = DataParser.parse_json(metadata.config_path)
	
	OnnxRunner.onnx_runner(metadata, config_data) 
