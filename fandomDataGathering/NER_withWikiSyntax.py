import pandas as pd
import re

def getData(text):
    matches = re.findall(r'\[\[(.*?)\]\]', text)
    named_entities = []
    categories = []
    files = []
    for match in matches:
        if ":" in match:
            if "File" in match:
                files.append(match.split("|")[0].split(":")[1])
            if "Category" in match:
                categories.append(match.split(":")[1])
        elif "|" in match:
            named_entities.append(match.split("|")[0])
        else:
            named_entities.append(match)
    return named_entities, files, categories

path = "../dok/fandomData.csv"
df = pd.read_csv(path)
print(df.head())

newDf = pd.DataFrame(columns=["title", "named_entities", "files", "categories"])


for _, row in df.iterrows():
    text = row['text']
    named_entities, files, categories = getData(text)
    new_row = {'title':"", 'named_entities': named_entities, 'files': files, 'categories': categories}
    newDf = newDf._append(new_row, ignore_index=True)

newDf['title'] = df.title

newDf.to_csv("../dok/fandomData_NER_withWikiSyntax.csv", index=False)
print(newDf)