import spacy
import numpy as np
import pandas as pd

nlp = spacy.load('en_core_web_trf')

path = "../dok/fandomData_NER_withSpacy.csv"
df = pd.read_csv(path)

ents = df['named_entities']
listOfEnts = []

for index, row in df.iterrows():
    boole = False
    try:
        x = float(row['named_entities'])
    except ValueError:
        boole = True

    if boole:
        print("skipped")
    else:
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
        print(index)
        if len(ents) > 0:
        #listOfEnts.append(ents)
            df.loc[index, 'named_entities'] = [ents]

        df.to_csv("../dok/fandomData_NER_withSpacy.csv", index=False)

df.to_csv("../dok/fandomData_NER_withSpacy.csv", index=False)
print(df)
