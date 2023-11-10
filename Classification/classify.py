import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "./resources")
from resources.preprocessing import preprocess, vectorize_dataset
from resources.setup import get_setup
from resources.model import Model, chunk_it_predictions, determine_ranks_and_save
from resources.get_data import get_current_data, make_dataset

def data_pipeline(corpus): 
    # setup
    configuration = get_setup(corpus)
    print("Configuration finished")
    # get_dataset
    df_eco, df_non_eco, df_rest = get_current_data(configuration)
    df = make_dataset(configuration, df_eco, df_non_eco)
    print(f"Dataset of {len(df)} samples")
    print(df['label'].value_counts())
    # preprocessing
    df = preprocess(configuration, df)
    train_ngram_x, train_y, test_ngram_x, test_y, scaler, vectorizer, selector = vectorize_dataset(configuration, df)
    print("Preprocessing ended")
    # Model and prediction
    lr = Model(train_ngram_x, train_y, test_ngram_x, test_y)
    with pd.option_context('mode.chained_assignment', None):
        proba = np.concatenate([x for x in chunk_it_predictions(lr, df_rest, 500, vectorizer, selector, scaler, configuration)])
    df_rest['proba'] = proba
    return pd.concat([df_rest, df_eco])