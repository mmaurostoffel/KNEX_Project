import pandas as pd
import re

def cleanEntities(text):
    # set to lowercase
    text = text.lower()

    #remove leading '
    text = text.strip("'")
    text = text.strip()

    return text

df = pd.read_csv("../dok/fandomData_NER_withWikiSyntax.csv")
print(df.head())


#clean Entity names
fullList_entity = []
titleList = []
for index, row in df.iterrows():
    print(index)
    title = row['title']
    clean = re.sub(r"\\", "", row["named_entities"])
    clean = re.sub(r'"', "'", clean)
    #matches = re.findall(r"'(.*?)'", clean)
    matches = clean.split(', ')
    for match in matches:
        match = re.sub(r"'", "", match)
        match = re.sub(r"]", "", match)
        match = re.sub(r"\[", "", match)
        fullList_entity.append(match)
        titleList.append(title)

# Create fullWikiEntityList
#create empty tag list
fullList_Tag = "" * len(fullList_entity)

data = pd.DataFrame({'entity': fullList_entity, 'tag': fullList_Tag}, columns=['entity', 'tag'])

#clean Entity names
cleanList_entity = []
for index, row in data.iterrows():
    cleanList_entity.append(cleanEntities(row.entity))
data['clean_entities'] = cleanList_entity


#Remove new duplicates
data = data.drop_duplicates(['clean_entities'])

data.to_csv("../dok/fullWikiEntityList.csv", index=False)
print(data)

# Create relationsList
relData = pd.DataFrame({'title': titleList, 'relatedTo': fullList_entity}, columns=['title', 'relatedTo'])
relData = relData.drop_duplicates()
relData.to_csv("../dok/relationList.csv", index=False)
print(relData)