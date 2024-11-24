import pandas as pd
from rdflib import Graph
from rdflib.namespace import RDFS

def cleanName(name):
    name = name.lower()
    return name


dfWiki = pd.read_csv("../dok/fullWikiEntityList.csv")
print(dfWiki.head())


g = Graph()
g.parse("../dok/base.ttl", format="turtle")

dfWikiBefore = dfWiki
liste = []
for url, _, name in g.triples((None, RDFS.label, None)):
    clean_Name =cleanName(name.value)
    if clean_Name in dfWiki.clean_entities.to_list():
        #Alle Namen, die das base.ttl bereits abdecken werden aus der WikiListe entfernt

        liste.append(clean_Name)

dfWiki = dfWiki[~dfWiki['clean_entities'].isin(liste)]
dfWikiAfter = dfWiki
print(liste)
print(len(dfWikiAfter), len(dfWikiBefore))
dfWiki.to_csv("../dok/WikiEntityList_withoutBase.csv", index=False)


