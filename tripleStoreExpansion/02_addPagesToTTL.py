import pandas as pd
from rdflib import Graph, URIRef, Namespace, RDFS, Literal
import urllib.parse

# Step 1: Create new Triplets
dfFandom = pd.read_csv("../dok/fandomDataCleaned.csv")
print(dfFandom.head())

g = Graph()
baseURL = "https://www.fhgr.ch/master/KE/2024/"
MYO = Namespace("https://www.fhgr.ch/master/KE/2024/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("myo", MYO)

for row in dfFandom.iterrows():
    title = row[1]['title']
    entity = MYO[urllib.parse.quote(title)]


    tag = URIRef(row[1]['link'])

    # WDT.P856 Official Website
    g.add((entity, WDT.P856, tag))
    # RDFS Label Title
    g.add((entity, RDFS.label, Literal(title)))


g.serialize('../results/pages.ttl', format='ttl')