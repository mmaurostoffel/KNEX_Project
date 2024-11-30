import pandas as pd
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer

def remove_stopwords_de(text,tokenizer, stopwords):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    filtered_tokens = [token for token in tokens if token not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def cleanEntities(text):
    # set to lowercase
    text = text.lower()

    # remove double whitespaces
    text = re.sub('  ', ' ', text)

    #remove leading '
    text = text.strip("'")
    text = text.strip()

    return text


df = pd.read_csv("../dok/old/fandomData_NER_withSpacy.csv")
print(df.head())

fullList_entity = []
fullList_Tag = []
#Add all entities into List
nList = df.named_entities
for i in nList:
    boole = False
    try:
        x = float(i)
    except ValueError:
        boole = True

    if not boole:
        print("skipped")
    else:
        matches = re.findall(r'\((.*?)\)', i)
        for match in matches:
            split = match.split(",")
            fullList_entity.append(split[0].strip("'"))
            fullList_Tag.append(split[1].strip())


data = pd.DataFrame({'entity': fullList_entity, 'tag': fullList_Tag}, columns=['entity', 'tag'])

#keep only valid tags
valid_tags = ["'PERSON'", "'NORP'", "'ORG'", "'LOC'"]
data = data[data['tag'].isin(valid_tags)]

#clean Entity names
cleanList_entity = []
for index, row in data.iterrows():
    cleanList_entity.append(cleanEntities(row.entity))
data['clean_entities'] = cleanList_entity

#Remove new duplicates
data = data.drop_duplicates(['clean_entities'])

#Remove new empty
data = data.dropna(axis=0, how='any')

data.to_csv("../dok/fullSpacyEntityList.csv", index=False)
print(data)
