import string
import numpy as np

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

def preprocess(df, STOPWORDS, corpus):

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