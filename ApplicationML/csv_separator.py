import pandas as pd

def csv_separator(file):
    source_df = pd.read_csv(file)
    training_df = source_df.sample(frac=70/100)
    
    merged = pd.merge(source_df, training_df, how='left', left_index=True, right_index=True, indicator=True)
    testing_df = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
    
    testing_df.to_csv("testing_df.csv")
    training_df.to_csv("training_df.csv")

csv_separator("training_data.csv")