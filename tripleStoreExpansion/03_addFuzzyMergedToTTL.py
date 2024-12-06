import pandas as pd
from rdflib import Graph, URIRef, Namespace, RDFS, Literal
import urllib.parse


def mapTagToClass(tag):
    #["'PERSON'", "'NORP'", "'ORG'", "'LOC'", "'EVENT'"]
    match tag:
        case "'LOC'":
            # Location in a Fictional work Q15796005
            return WD.Q15796005
        case "'PERSON'":
            #Fictional Person Q15632617
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
dfMerged = pd.read_csv("../results/mergedEntityList_fuzzy_filtered.csv")
#dfWikiCopy = pd.read_csv("../dok/WikiEntityList_withoutBase.csv")
#dfSpacyCopy = pd.read_csv("../dok/fullSpacyEntityList.csv")

g = Graph()
baseURL = "https://www.fhgr.ch/master/KE/2024/"
MYO = Namespace("https://www.fhgr.ch/master/KE/2024/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("myo", MYO)

for row in dfMerged.iterrows():
    saved_Spacy_entity = row[1]['Spacy_entity']
    saved_Wiki_entity = row[1]['Wiki_entity']
    title = row[1]['Wiki_entity']
    entity = MYO[urllib.parse.quote(title)]

    tag = row[1]['Spacy_tag']
    rdfClass = mapTagToClass(tag)

    if rdfClass != 'unknown':
        # Add title of entity
        g.add((entity, RDFS.label, Literal(title)))
        # Add Class of entity
        g.add((entity, WDT.P31, rdfClass))


g.serialize('../results/fuzzyMerged.ttl', format='ttl')


