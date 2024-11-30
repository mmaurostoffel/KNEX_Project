import pandas as pd
from rdflib import Graph, URIRef, Namespace
import urllib.parse
import re

df = pd.read_csv("../dok/fandomData_NER_withWikiSyntax.csv")
print(df.head())
fileBaseURL = 'https://warhammer40k.fandom.com/wiki/File:'

g = Graph()
baseURL = "https://www.fhgr.ch/master/KE/2024/"
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("dc", DC)

for row in df.iterrows():
    entity = row[1]['title']
    entity = urllib.parse.quote(baseURL + entity)
    entity = URIRef(entity)


    files = row[1]['files']
    files = files.split(',')

    for file in files:
        out = re.findall("'([^']*)'", file)
        try:
            temp = out[0]
        except:
            out = re.findall('"([^"]*)"', file)

        if len(out) == 1:
            file = urllib.parse.quote(out[0])
            fileUrl = URIRef(fileBaseURL + file)
        else: pass

        # dc:related
        g.add((entity, DC.related, fileUrl))
g.serialize('../results/files.ttl', format='ttl')