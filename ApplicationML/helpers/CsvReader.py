import pandas as pd

class CsvReader:
    def __init__(self):
        pass

    def csv_separator(file_path):
    	df = pd.read_csv(file_path)

    	seventy_percent = int(0.7 * len(df))

    	training_df = df.iloc[:seventy_percent]
    	testing_df = df.iloc[seventy_percent:]

    	training_file_path = 'training_file.csv'
    	testing_file_path = 'testing_file.csv'

    	training_df.to_csv(training_file_path, index=False)
    	testing_df.to_csv(testing_file_path, index=False)

    	return training_df, testing_df
