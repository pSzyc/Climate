import pandas as pd

def get_current_data(configuration):
    drive_path = configuration.drive_path
    corpus = configuration.corpus
    df_eco = pd.read_csv(drive_path / corpus / "eco_result.csv", index_col=['id', 'source'], parse_dates=['date'])
    df_non_eco = pd.read_csv(drive_path / corpus / "non_eco_result.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_rest = pd.read_csv(drive_path / corpus / "results.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_eco['label'] = 1
    df_non_eco['label'] = 0
    return df_eco, df_non_eco, df_rest

def make_dataset(configuration, df_eco, df_non_eco):
    if configuration.corpus == "rzepa":
        df = pd.concat([df_eco, df_non_eco])
    else:
        df_7 = pd.read_csv(configuration.drive_path  / "dataset_7.csv", index_col = ['id', 'source'])
        df_sample = df_7.sample(n = 10000)
        df = pd.concat([df_eco, df_non_eco, df_sample])
    return df