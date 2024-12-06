import pandas as pd
from rdflib import Graph, URIRef, Namespace, RDFS, Literal
import urllib.parse

# Step 1: Create new Triplets
dfFandom = pd.read_csv("../dok/relationList.csv")
print(dfFandom.head())

g = Graph()
baseURL = "https://www.fhgr.ch/master/KE/2024/"
MYO = Namespace("https://www.fhgr.ch/master/KE/2024/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("dc", DC)
g.bind("myo", MYO)

for row in dfFandom.iterrows():
    entTitle = row[1]['title']
    entity = MYO[urllib.parse.quote(entTitle)]

    relatedToTitle = row[1]['relatedTo']
    if isinstance(relatedToTitle, float):
        continue
    relatedTo = MYO[urllib.parse.quote(relatedToTitle)]

    # entity dc:related to relation
    g.add((entity, DC.related, relatedTo))
    # RDFS Label Title für Entity und Relation
    g.add((entity, RDFS.label, Literal(entTitle)))
    g.add((relatedTo, RDFS.label, Literal(relatedToTitle)))


g.serialize('../results/relations.ttl', format='ttl')