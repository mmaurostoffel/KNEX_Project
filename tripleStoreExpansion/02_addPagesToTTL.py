import pandas as pd
from rdflib import Graph, URIRef, Namespace
import urllib.parse

# Step 1: Create new Triplets
dfFandom = pd.read_csv("../dok/fandomDataCleaned.csv")
print(dfFandom.head())

g = Graph()
baseURL = "https://www.fhgr.ch/master/KE/2024/"
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
g.bind("wdt", WDT)
g.bind("wd", WD)

for row in dfFandom.iterrows():
    # row 1 = Wiki Entity, row 3 = Spacy Tag
    entity = row[1]['title']
    entity = urllib.parse.quote(baseURL + entity)
    entity = URIRef(entity)


    tag = URIRef(row[1]['link'])

    # WDT.P856 Official Website
    g.add((entity, WDT.P856, tag))


g.serialize('../results/pages.ttl', format='ttl')