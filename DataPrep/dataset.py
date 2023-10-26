import pandas as pd
import numpy as np
from pathlib import Path

source_dict = {
    "rzepa": "Rzeczypospolita",
    'gpc': "Gazeta Polska Codziennie",
    'newsweek': "Newsweek",
    'wprost' : 'Wprost',
    'dorzeczy': "DoRzeczy",
    "polityka" : "Polityka"
}
files_path = Path("/home/hombre/Code/Climate Project/Classification/files")
drive_path = Path("/run/user/1000/gvfs/google-drive:host=gmail.com,user=przemek.7678/0ACbMJp-uzuEwUk9PVA/1z7kfn_M6wSuIPxoQ_MoS2NlJgVRqyYyC/")
corpus_path = Path("/run/user/1000/gvfs/google-drive:host=gmail.com,user=przemek.7678/GVfsSharedDrives/0AAcFxORfkRfDUk9PVA/13iaeWwq4Ci83lCggiCuLvcIHCSfREE0P/14CVZXy2f6ObWorvYy_xyhSRjIcQAW1nY")

df_list = []

for coprus in source_dict.keys():
    df_eco = pd.read_csv(drive_path / coprus / "eco_all.csv")
    df_eco.to_csv( files_path / f"eco_{coprus}.csv", index=False)
    df_non_eco = pd.read_csv(drive_path / coprus / "non_eco_result.csv")
    df_eco['label'] = 1
    df_non_eco['label'] = 0
    df = pd.concat([df_eco[df_eco['rank'] != 4], df_non_eco])
    df['source'] = source_dict[coprus]
    #df = df[['id','source','text','title', 'clean_text','vectorized', 'clean_title','label', 'date']]
    df_list.append(df)
    
dataset = pd.concat(df_list)
dataset.to_csv(drive_path /'dataset_7.csv', index=False)