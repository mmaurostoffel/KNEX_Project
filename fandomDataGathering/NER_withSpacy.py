import spacy
import numpy as np
import pandas as pd

nlp = spacy.load('en_core_web_trf')

path = "../dok/fandomDataCleaned.csv"
df = pd.read_csv(path)

emptyList = [""] * len(df)
df['named_entities'] = emptyList

listOfEnts = []
for index, row in df.iterrows():
    ents = []
    text = row['cleanText']
    doc = nlp(text)
    #Get entities
    for ent in doc.ents:
        #put ents into list
        ents.append((ent.text, ent.label_))

    #remove duplicates
    ents = list(set(ents))
    print(ents)
    #listOfEnts.append(ents)
    df.loc[index, 'named_entities'] = [ents]

    df.to_csv("../dok/fandomData_NER_withSpacy.csv", index=False)

df.to_csv("../dok/fandomData_NER_withSpacy.csv", index=False)
print(df)
