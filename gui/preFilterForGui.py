import streamlit as st
from rdflib import Graph, URIRef, Namespace, RDFS
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore

g = Graph()
g.parse("results/fullTripleStore_expanded.ttl", format="turtle")

WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
MYO = Namespace("https://www.fhgr.ch/master/KE/2024/")
SCHEMA = Namespace("http://schema.org/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("dc", DC)
g.bind("schema", SCHEMA)
g.bind("myo", MYO)



g2 = Graph()
g2.bind("wdt", WDT)
g2.bind("wd", WD)
g2.bind("dc", DC)
g2.bind("schema", SCHEMA)
g2.bind("myo", MYO)

# Vorfiltern
# alle Nodes mit Page auswählen
nodeWithPage = []
for s, o, p in g.triples((None, WDT.P856, None)):
    nodeWithPage.append(s)
print("Loading done")
# Alle Inhalte aller Nodes mit Files in neuen TripleStore aufnehmen
for s, o, p in g.triples((None, None, None)):
    if s in nodeWithPage:
        g2.add((s, o, p))
print("Loading 2 done")


g3 = Graph()
g3.bind("wdt", WDT)
g3.bind("wd", WD)
g3.bind("dc", DC)
g3.bind("schema", SCHEMA)
g3.bind("myo", MYO)

# alle Nodes mit Class auswählen
nodeWithClass = []
for s, o, p in g2.triples((None, WDT.P31, None)):
    nodeWithClass.append(s)
print("Loading done")
# Alle Inhalte aller Nodes mit Files in neuen TripleStore aufnehmen
for s, o, p in g2.triples((None, None, None)):
    if s in nodeWithClass:
        g3.add((s, o, p))
print("Loading 2 done")


# Add back all Labels
for s, o, p in g.triples((None, RDFS.label, None)):
    g3.add((s, o, p))

g3.serialize('../results/expandedFiltered.ttl', format='ttl')

