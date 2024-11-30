import pandas as pd
from fuzzywuzzy import fuzz


dfWiki = pd.read_csv("../dok/WikiEntityList_withoutMerged.csv")
dfWikiCopy = pd.read_csv("../dok/WikiEntityList_withoutMerged.csv")

dfSpacy = pd.read_csv("../dok/fullSpacyEntityList_withoutMerged.csv")
dfSpacyCopy = pd.read_csv("../dok/fullSpacyEntityList_withoutMerged.csv")

print(dfWikiCopy.head())
data = []
for index, rowWiki in dfWiki.iterrows():
    print(index, "of", len(dfWiki))
    for index, rowSpacy in dfSpacy.iterrows():
        if type(rowWiki['clean_entities']) == str and type(rowSpacy['clean_entities']) == str:
            ratio = fuzz.ratio(rowWiki['clean_entities'], rowSpacy['clean_entities'])
            if ratio > 80:
                print(rowWiki['clean_entities'], rowSpacy['clean_entities'])
                data.append([ratio, rowSpacy['entity'], rowSpacy['tag'], rowSpacy['clean_entities'], rowWiki['entity'], rowWiki['tag'], rowWiki['clean_entities']])
                dfWikiCopy.drop(dfWikiCopy[dfWikiCopy['entity'] == rowWiki['entity']].index, inplace=True)
                dfSpacyCopy.drop(dfSpacyCopy[dfSpacyCopy['entity'] == rowSpacy['entity']].index, inplace=True)
        else:
            #print("not ok")
            continue

df = pd.DataFrame(data, columns=['ratio', 'Spacy_entity', 'Spacy_tag', 'Spacy_clean_entities', 'Wiki_entity', 'Wiki_tag', 'Wiki_clean_entities'])
df.to_csv("../results/mergedEntityList_fuzzy.csv", index=False)
dfWikiCopy.to_csv("../dok/WikiEntityList_withoutFuzzy.csv", index=False)
dfSpacyCopy.to_csv("../dok/fullSpacyEntityList_withoutFuzzy.csv", index=False)


