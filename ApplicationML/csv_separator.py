import pandas as pd

def csv_separator(file):
    source_df = pd.read_csv(file)
    #Put 70% of the source data in the training dataframe
    training_df = source_df.sample(frac=70/100)
    
    #Take the remaining data and put it in the testing dataframe
    merged = pd.merge(source_df, training_df, how='left', left_index=True, right_index=True, indicator=True)
    testing_df = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
    
    return training_df, testing_df