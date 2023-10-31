import string
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

NGRAM_RANGE = (1, 3)

TOP_K = 7500

TOKEN_MODE = 'word'

MIN_DOCUMENT_FREQUENCY = 5

def ngram_vectorize(train_texts, train_labels, val_texts, return_models = False):

    kwargs = {
            'ngram_range': NGRAM_RANGE,
            'dtype': np.float32, 
            'strip_accents': 'unicode',
            'decode_error': 'replace',
            'analyzer': TOKEN_MODE, 
            'min_df': MIN_DOCUMENT_FREQUENCY,
    }
    vectorizer = TfidfVectorizer(**kwargs)

    x_train = vectorizer.fit_transform(train_texts)

    x_val = vectorizer.transform(val_texts)

    selector = SelectKBest(f_classif, k=min(TOP_K, x_train.shape[1]))
    selector.fit(x_train, train_labels)
    x_train = selector.transform(x_train).astype(np.float32)
    x_val = selector.transform(x_val).astype(np.float32)

    x_train = x_train.toarray()
    x_val = x_val.toarray()

    if return_models:
        return  x_train, x_val, vectorizer, selector
    else:
        return x_train, x_val

def vectorize(data, vectorizer, selector):
    data = vectorizer.transform(data)
    data = selector.transform(data).astype(np.float32)
    return data.toarray()

def meta_features(data, STOPWORDS):
  # word_count
  data['Całkowita ilość słów'] = data['text'].apply(lambda x: len(str(x).split()))
  data['Ilość słów bez powtórzeń'] = data['text'].apply(lambda x: len(set(str(x).split())))

  # stop_word_count
  data['Ilość stop-słów'] = data['text'].apply(lambda x: len([w for w in str(x).lower().split() if w in STOPWORDS]))

  # mean_word_length
  data['Średnia długość słowa'] = data['text'].apply(lambda x: np.mean([len(w) for w in str(x).split()]))

  # char_count
  data['Ilość symboli'] = data['text'].apply(lambda x: len(str(x)))

  # punctuation_count
  data['Ilość znaków interpunkcyjnych'] = data['text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))
  return data


def feature_engineering(df):

  zycie = ['Życie Rzeszowa i Podkarpacia',
  'Życie Regionów',
  'Życie Pomorza',
  'Życie Wielkopolski',
  'Życie Krakowa i Małopolski',
  'Życie Dolnego Śląska',
  'Życie Szczecina i Pomorza Zachodniego',
  'Życie Kujawsko-Pomorskigo',
  'Życie Ziemi Łódzkiej',
  'Życie Śląska',
  'Życie Lubelszczyzny',
  'Życie Ziemi Podlaskiej',
  'Życie Opola i Ziemi Opolskiej',
  'Życie Mazowsza',
  'Życie Ziemi Świętokrzyskiej',
  'Życie Pomorza Zachodniego']

  df['department'].replace(['Prawo co dnia', 'Prawo w biznesie','Rzecz o prawie'], 'Prawo', inplace=True)
  df['department'].replace(zycie + ['Kraj','Świat'],"Region", inplace=True)
  df['department'].replace(['Plus Minus', 'Komentarze','Publicystyka, Opinie'], 'Opinie', inplace=True)
  df['department'].replace(['Kadry i Płace', 'Praca i ZUS','Sądy i Prokuratura',"Administracja – Orzecznictwo"], 'Administracja', inplace=True)
  df['department'].replace(['Pierwsza strona','Druga strona','Trzecia strona'], 'Strona 123', inplace=True)
  df['department'].replace(['Biznes w czasie pandemii','Biznes i finanse','Dobra Firma','Nieruchomości','Moje pieniądze','Rachunkowość','Ekspert księgowego','Podatki i księgowość', 'Administracja','Dobra Administracja','Podatki',"Biznes"],'Pieniądze', inplace=True)
  df['department'].replace(['Nauka','Rzecz o zdrowiu'],'Nauka i zdrowie', inplace=True)
  df['department'].replace(['Biznes odpowiedzialny w Polsce', "Walczymy ze smogiem", "Walka o klimat. Wyzwania dla Polski, Europy i Świata", "CSR Społeczna", "Gospodarka obiegu", "CSR- Pomagamy!", ""], "Eco",  inplace=True)
  df['department'].replace(['Kultura','Sport'],'Sport i kultura', inplace=True)
  df['department'].replace(['Nieruchomości w Ekonomii','Sport'],'Sport i kultura', inplace=True)
  df['department'].replace(['Energia i biznes','Energia dla domu i firmy'],'Energetyka', inplace=True)

  return df

def vectorized_retriver(row):
  vectorized =  row['vectorized'][1:-1].split(",")
  row['ngram_sum'] = float(vectorized[-1])
  row['ngram_sum_squared'] = float(vectorized[-2])
  row['ngram_sum_to_total'] = float(vectorized[-3])
  row['ngram_sum_squared_to_total'] = float(vectorized[-4])
  row['ngram_weak_ngrams'] = float(vectorized[-5])

  return row

def vectorize_dataset(configuration, df):
    METAFEATURES = configuration.METAFEATURES
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

def preprocess(df, configuration):
  STOPWORDS = configuration.STOPWORDS
  #if corpus not in ['wprost', 'dorzeczy']:
  #
  #  df['department'] = df['department'].replace("None", "Inne")
  #  df['department'] = df['department'].replace("NONE", "Inne")
  #  df['department'] = df['department'].fillna("Inne")
  #  df.loc[df.groupby('department')['department'].transform('size')<50, 'department'] = 'Inne'
  #
  #  df['author'] = df['author'].replace("None", "Inne")
  #  df['author'] = df['author'].replace("NONE", "Inne")
  #  df['author'] = df['author'].fillna("Inne")
  #  df.loc[df.groupby('author')['author'].transform('size')<75, 'author'] = 'Inne'
  #  df = feature_engineering(df)

  df = meta_features(df, STOPWORDS)
  
  if not all(col in df.columns.values for col in ["ngram_sum", "ngram_sum_to_total", "ngram_sum_squared" , "ngram_sum_squared_to_total"]):
    df = df.apply(vectorized_retriver, axis=1)
  
  try:
    df['year'] = df.date.dt.year.astype(str)
  except:
    df['year'] = 'None'

  return df