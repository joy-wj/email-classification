import pandas as pd
import numpy as np
from pathlib import Path
import sys
import pickle

if __name__ == '__main__':

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    model_name = '../model/saved_models/RF_model_features.sav'
    loaded_model = pickle.load(open(model_name, 'rb'))

    # Read table with DNS records and scraped data
    df = pd.read_csv('../data/test_combined.csv')

    # read a list of input domain names
    df_input = pd.read_csv(input_path)
    domains = df_input['domain'].to_frame()

    # extract matched data from database
    data = pd.merge(domains, df, how="inner", on='domain')
    
    # Predict
    X = data.drop(['domain', 'tld', 'label'], axis=1)
    domains['trusted_proba'] = loaded_model.predict_proba(X)[:,0]
    domains['prediction'] = loaded_model.predict(X)

    domains.to_csv(output_path, index=False)
