import pandas as pd
import numpy as np
from resources.preprocessing import preprocess, vectorize_dataset
from resources.setup import get_setup
from resources.model import Model, chunk_it_predictions, determine_ranks_and_save
from resources.get_data import get_current_data, make_dataset, get_rest_of_data

# setup
configuration = get_setup()

# get_dataset
df_eco, df_non_eco = get_current_data(configuration.corpus, configuration.drive_path)
df_eco, df = make_dataset(configuration, df_eco, df_non_eco)
df_rest = get_rest_of_data(configuration)

# preprocessing
df = preprocess(df, configuration.STOPWORDS, configuration.corpus)
train_ngram_x, train_y, test_ngram_x, test_y, scaler, vectorizer, selector = vectorize_dataset(df, configuration.METAFEATURES)

# Model and prediction
lr = Model(train_ngram_x, train_y, test_ngram_x, test_y)
with pd.option_context('mode.chained_assignment', None):
    proba = np.concatenate([x for x in chunk_it_predictions(df_rest, 500)])
determine_ranks_and_save(configuration, df_eco, df_rest, proba)