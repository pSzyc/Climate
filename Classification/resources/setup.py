from pathlib import Path
import pandas as pd

class config:
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

    METAFEATURES = [
        'Całkowita ilość słów',
        'Ilość słów bez powtórzeń',
        'Ilość stop-słów',
        'Średnia długość słowa',
        'Ilość symboli',
        'Ilość znaków interpunkcyjnych'
    ]

    def __init__(self, corpus, drive_path, files_path, STOPWORDS):
        self.corpus = corpus
        self.drive_path = drive_path
        self.files_path = files_path
        self.STOPWORDS = STOPWORDS


def get_current_data(corpus, drive_path):
    df_eco = pd.read_csv(drive_path / corpus / "eco_result.csv", index_col=['id', 'source'], parse_dates=['date'])
    df_non_eco = pd.read_csv(drive_path / corpus / "non_eco_result.csv", index_col = ['id', 'source'], parse_dates=['date'])
    df_eco['label'] = 1
    df_non_eco['label'] = 0
    return df_eco,df_non_eco

def get_setup():
    corpus = input("Please provide corpus:")
    drive_path = input("Please provide drive path:")
    drive_path = Path(drive_path)
    files_path = Path("/home/hombre/Code/Climate Project/Classification/files")
    stopwords = pd.read_csv( files_path / 'polish_stopwords.txt', header=None)
    STOPWORDS = set([word.rstrip() for word in stopwords[0]])
    configuration = config(corpus, drive_path, files_path, STOPWORDS)
    return configuration