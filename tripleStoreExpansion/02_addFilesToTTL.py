import pandas as pd
from rdflib import Graph, URIRef, Namespace, Literal
import urllib.parse
import re

df = pd.read_csv("../dok/fandomData_NER_withWikiSyntax.csv")
print(df.head())
fileBaseURL = 'https://warhammer40k.fandom.com/wiki/File:'

g = Graph()
baseURL = "https://www.fhgr.ch/master/KE/2024/"
MYO = Namespace("https://www.fhgr.ch/master/KE/2024/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
SCHEMA = Namespace("http://schema.org/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("schema", SCHEMA)
g.bind("myo", MYO)

for row in df.iterrows():
    entity = row[1]['title']
    entity = MYO[urllib.parse.quote(entity)]


    files = row[1]['files']
    files = files.split(',')

    for file in files:
        out = re.findall("'([^']*)'", file)
        try:
            temp = out[0]
        except:
            out = re.findall('"([^"]*)"', file)

        if len(out) == 1:
            #file = urllib.parse.quote(out[0])
            #fileUrl = URIRef(fileBaseURL + file)
            file = out[0]
        else: pass

        # dc:related
        #g.add((entity, SCHEMA.associatedMedia, fileUrl))
        g.add((entity, SCHEMA.associatedMedia, Literal(file)))
g.serialize('../results/files.ttl', format='ttl')