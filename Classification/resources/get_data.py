import pandas as pd

def get_current_data(configuration):
    drive_path = configuration.drive_path
    corpus = configuration.corpus
    df_eco = pd.read_csv(drive_path / corpus / "eco_result.csv", index_col=['id', 'source'], parse_dates=['date'])
    df_non_eco = pd.read_csv(drive_path / corpus / "non_eco_result.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_eco['label'] = 1
    df_non_eco['label'] = 0
    return df_eco,df_non_eco

def make_dataset(configuration, df_eco, df_non_eco):
    if configuration.corpus == "rzepa":
        df_5 = pd.read_csv(configuration.drive_path  / "dataset_6_all.csv", index_col = ['id', 'source'])
        df_5.rename(columns={ "class": "label"}, inplace=True)
        df_5 = df_5[df_5['translated'] == 0]
        df_eco['translated'] = 0
        df_non_eco['translated'] = 0
        df_eco = df_eco[~df_eco.index.isin(df_5.index)]
        df_non_eco = df_non_eco[~df_non_eco.index.isin(df_5.index)].sample(n = len(df_eco))
        df = pd.concat([df_eco, df_non_eco, df_5])
    else:
        df_7 = pd.read_csv(configuration.drive_path  / "dataset_7.csv", index_col = ['id', 'source'])
        df_sample = df_7.sample(n = 10000)
        df = pd.concat([df_eco, df_non_eco, df_sample])
    return df

def get_rest_of_data(configuration):
    if configuration.corpus == "rzepa":
        df_rest = pd.read_csv(configuration.drive_path / configuration.corpus / "results.csv", index_col = ['id', 'source'], parse_dates=['date'])
    else: 
        df_rest = pd.read_csv(configuration.drive_path / configuration.corpus / "results.csv", index_col = ['id', 'source'], parse_dates=['date'])
    return df_rest