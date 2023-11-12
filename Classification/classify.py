import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "./resources")
from resources.preprocessing import preprocess, vectorize_dataset
from resources.setup import get_setup
from resources.model import Model, chunk_it_predictions
from resources.get_data import get_current_data, make_dataset
from functools import reduce

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

def eco_selector(df):
    df['klimat_count'] = df['ngram_sum'] * df['klimat']
    condition_list_1 = [
        df['ngram_sum_squared_to_total'] > 0.75,
        df['proba'] > 0.5,
        df['weak_count'] < 0.5
    ]
    condition_list_2 = [
        df['weak_count']  < 0.3,
        df['ngram_sum_squared_to_total'] > 0.5,
        df['num_words'] > 2,
        df['proba'] > 0.5
    ]
    condition_list_3 = [
        df['klimat_count'] > 2,
        df['ngram_sum_squared_to_total'] > 0.33,
    ]
    condition_list_4 = [
        df['klimat_count'] > 0,
        df['proba'] > 0.8,
        df['weak_count'] < 0.5,
        df['num_words'] > 2
    ]
    selector = lambda condition_list: reduce(lambda x, y: x & y, condition_list)
    mask = selector(condition_list_1) | selector(condition_list_2) | selector(condition_list_3) | selector(condition_list_4)
    return df[mask]

def filter_by_conditions(df, condition_list):
    condition_list.append(df['Rank'].isna())
    selection_mask = reduce(lambda x, y: x & y, condition_list)
    df.loc[selection_mask, 'Rank'] = 'Test'
    print(len(df[selection_mask]))
    if len(df[selection_mask]) > 100:
        print('Saving')
        df[selection_mask].sample(100).to_csv("data_test.csv")
    else:
        df[selection_mask].to_csv("data_test.csv")
    return df

def approve(df, name):
    df.loc[df['Rank'] == 'Test', 'Rank'] = name
    return df

def restore(df):
    df.loc[df['Rank'] == 'Test', 'Rank'] = None
    return df