import pandas as pd
from pathlib import Path

def get_current_data(configuration):
    drive_path = configuration.drive_path
    corpus = configuration.corpus
    df_eco = pd.read_csv(drive_path / corpus / "eco_result.csv", index_col=['id', 'source'], parse_dates=['date'])
    df_non_eco = pd.read_csv(drive_path / corpus / "non_eco_result.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_rest = pd.read_csv(drive_path / corpus / "results.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_eco['label'] = 1
    df_non_eco['label'] = 0
    df_eco = df_eco.fillna("None")
    df_non_eco = df_non_eco.fillna("None")
    df_rest = df_rest.fillna("None")
    return df_eco, df_non_eco, df_rest

def make_dataset(configuration, df_eco, df_non_eco):
    drive_path = configuration.drive_path
    corpus = configuration.corpus

    if corpus == "rzepa":
        df = pd.concat([df_eco, df_non_eco])
    else:
        df_eco_rzepa = pd.read_csv(drive_path / "rzepa" / "eco_rzepa.csv", index_col=['id', 'source'], parse_dates=['date'])
        df_non_eco_rzepa = pd.read_csv(drive_path / "rzepa" / "non_eco_result.csv", index_col = ['id', 'source'], parse_dates=['date'])
        df_eco_rzepa['label'] = 1
        df_non_eco_rzepa['label'] = 0
        df = pd.concat([df_eco, df_eco, df_non_eco, df_non_eco, df_eco_rzepa, df_non_eco_rzepa])
    return df