import pandas as pd

dfSpacy = pd.read_csv("../dok/fullSpacyEntityList.csv")
dfSpacy = dfSpacy.rename(columns={"entity": "Spacy_entity", "tag": "Spacy_tag"})
print(dfSpacy.head())

#Hier wird die ..._withoutBase Liste verwendet, da in diesem Arbeisschritt die base daten entfernt wurden und nicht mehr
#gematcht werden müssen
dfWiki = pd.read_csv("../dok/WikiEntityList_withoutBase.csv")
dfWiki = dfWiki.rename(columns={"entity": "Wiki_entity", "tag": "Wiki_tag"})
print(dfWiki.head())

merged = pd.merge(dfSpacy, dfWiki, on="clean_entities")
print(merged.head())

merged.to_csv("../results/mergedEntityList.csv", index=False)