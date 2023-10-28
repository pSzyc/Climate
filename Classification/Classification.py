import pandas as pd
import numpy as np
from pathlib import Path
from preprocessing import preprocess
from models import ngram_vectorize, vectorize
from tqdm import tqdm
from math import ceil
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import sys

source_dict = {
    "rzepa": "Rzeczypospolita",
    'gpc': "Gazeta Polska Codziennie",
    'newsweek': "Newsweek",
    'wprost' : 'Wprost',
    'dorzeczy': "DoRzeczy",
    'polityka': "Polityka",
    'wyborcza': "Gazeta Wyborcza",
    "wpolityce": "wPolityce"
}

METAFEATURES = ['Całkowita ilość słów', 'Ilość słów bez powtórzeń', 'Ilość stop-słów', 'Średnia długość słowa',
                'Ilość symboli', 'Ilość znaków interpunkcyjnych']

lr_best = {'C': 15.612022973907699, 'penalty': 'l1', 'solver':'liblinear'}


def get_setup():
    corpus = sys.argv[1]
    drive_path = input("Please provide drive path:")
    drive_path = Path(drive_path)
    files_path = Path("/home/hombre/Code/Climate Project/Classification/files")
    stopwords = pd.read_csv( files_path / 'polish_stopwords.txt', header=None)
    STOPWORDS = set([word.rstrip() for word in stopwords[0]])
    return corpus, drive_path, STOPWORDS

def get_training_data():
    df_train, df_test = train_test_split(df, test_size=0.1)
    scaler = StandardScaler()
    meta_train = scaler.fit_transform(df_train[METAFEATURES])
    meta_test = scaler.transform(df_test[METAFEATURES])
    train_x = df_train.drop(columns=['label'])
    train_y = df_train['label']

    test_x = df_test.drop(columns=['label'])
    test_y = df_test['label']

    text_train, text_test, vectorizer, selector = ngram_vectorize(train_x['clean_text'], train_y, test_x['clean_text'],return_models=True)
    train_ngram_x  = np.concatenate([text_train, meta_train], axis=1)
    test_ngram_x  = np.concatenate([text_test, meta_test], axis=1)
    return train_ngram_x, train_y, test_ngram_x, test_y, scaler, vectorizer, selector


def get_current_data(corpus, drive_path):
    df_eco = pd.read_csv(drive_path / corpus / "eco_result.csv", index_col=['id', 'source'], parse_dates=['date'])
    df_non_eco = pd.read_csv(drive_path / corpus / "non_eco_result.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_eco['label'] = 1
    df_non_eco['label'] = 0
    return df_eco,df_non_eco
    
def Model(params, train_x, train_y, test_x, test_y)
    lr = LogisticRegression(**params)
    lr.fit(train_x, train_y)
    predicted_lr = lr.predict_proba(test_x)[:, 1]
    y_pred = predicted_lr > .5
    print("Accuracy of model", accuracy_score(y_pred=y_pred, y_true=test_y))
    return lr

def chunk_it_predictions(data, size):
    chunks = ceil(len(data) / size)
    for i in tqdm(range(chunks)):
        chunk = df_rest.iloc[i * size : (i+1) * size]
        chunk = preprocess(chunk, STOPWORDS, corpus)
        meta_rest = scaler.transform(chunk[METAFEATURES])
        rest_text = vectorize(chunk['clean_text'], vectorizer, selector)
        rest_ngram_x =  np.concatenate([rest_text, meta_rest], axis=1)
        predicted_lr = lr.predict_proba(rest_ngram_x)[:, 1]
        yield predicted_lr

corpus, drive_path, STOPWORDS = get_setup()

df_eco, df_non_eco = get_current_data(corpus, drive_path)
    
if corpus == "rzepa":
    df_5 = pd.read_csv(drive_path  / "dataset_6_all.csv", index_col = ['id', 'source'])
    df_5.rename(columns={ "class": "label"}, inplace=True)
    df_5 = df_5[df_5['translated'] == 0]
    df_eco['translated'] = 0
    df_non_eco['translated'] = 0
    df_eco = df_eco[~df_eco.index.isin(df_5.index)]
    df_non_eco = df_non_eco[~df_non_eco.index.isin(df_5.index)].sample(n = len(df_eco))
    df = pd.concat([df_eco, df_non_eco, df_5])
else:
    df_7 = pd.read_csv(drive_path  / "dataset_7.csv", index_col = ['id', 'source'])
    df_sample = df_7.sample(n = 10000)
    df = pd.concat([df_eco, df_non_eco, df_sample])

    
df = preprocess(df, STOPWORDS, corpus)
train_ngram_x, train_y, test_ngram_x, test_y, scaler, vectorizer, selector = get_training_data()

lr = Model(lr_best, train_ngram_x, train_y, test_ngram_x, test_y)

if corpus == "rzepa":
    df_rest = pd.read_csv(drive_path / corpus / "results.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_rest = df_rest[~df_rest.index.isin(df_5.index)]
else: 
    df_rest = pd.read_csv(drive_path / corpus / "results.csv", index_col = ['id', 'source'], parse_dates=['date'])

with pd.option_context('mode.chained_assignment', None):
    proba = np.concatenate([x for x in chunk_it_predictions(df_rest, 500)])

df_rest['proba'] = proba
df_rest['rank'] = 0
df_rest.loc[(df_rest['proba']>0.8) & (df_rest['ngram_sum_squared_to_total'] > 1), 'rank'] = 1
df_rest.loc[(df_rest['proba']>0.8) & (df_rest['ngram_sum_squared_to_total'] <  1), 'rank'] = 2
df_rest.loc[(df_rest['proba'].between(0.5, 0.8)) & (df_rest['ngram_sum_squared_to_total'] > 0.5), 'rank'] = 3
df_rest.loc[(df_rest['proba'].between(0.5, 0.8)) & (df_rest['ngram_sum_squared_to_total'] < 0.5), 'rank'] = 4
df_rest.loc[df_rest['rank'] != 0, 'label'] = 1
df_eco['rank'] = 1

try:
    df_eco.drop(columns=['translated'], inplace=True)
except:
    print("No translated documents found")

df_rest = df_rest[df_eco.columns.values]
df_final = pd.concat([df_rest[df_rest['rank'] != 0], df_eco])
df_rest.to_csv(drive_path / corpus /  f"results.csv")