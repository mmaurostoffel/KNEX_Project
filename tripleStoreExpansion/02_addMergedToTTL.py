import pandas as pd
from rdflib import Graph, URIRef, Namespace
import urllib.parse


def mapTagToClass(tag):
    #["'PERSON'", "'NORP'", "'ORG'", "'LOC'", "'EVENT'"]
    match tag:
        case "'LOC'":
            # Location in a Fictional work Q15796005
            return WD.Q15796005
        case "'PERSON'":
            #Fictional Person Q95074
            return WD.Q15632617
        case "'NORP'":
            # NORP # Nationalities or religious or political groups Q20667393
            # Warhammer race Q20667393
            return WD.Q20667393
        case "'ORG'":
            # Fictional Organisation Q14623646
            # Überklasse von fictional military organization Q18011141
            return WD.Q14623646
        case _:
            return 'unknown'


# Step 1: Create new Triplets
dfMerged = pd.read_csv("../results/mergedEntityList.csv")
print(dfMerged.head())

g = Graph()
baseURL = "www.fhgr.ch/master/KE/2024/"
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
g.bind("wdt", WDT)
g.bind("wd", WD)

for row in dfMerged.iterrows():
    # row 1 = Wiki Entity, row 3 = Spacy Tag
    entity = row[1]['Wiki_entity']
    entity = urllib.parse.quote(baseURL + entity)
    entity = URIRef(entity)

    tag = row[1]['Spacy_tag']
    rdfClass = mapTagToClass(tag)

    if rdfClass != 'unknown':
        g.add((entity, WDT.P31, rdfClass))


g.serialize('../results/merged.ttl', format='ttl')
# Step 2: Remove new Additions from mergedEntityList
