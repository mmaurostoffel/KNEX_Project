import streamlit as st
from rdflib import Graph, URIRef, Namespace, RDFS, Literal
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore


def generateLists(g):
    raceList, charList, orgList, locList = [],[],[],[]

    for s,_,o in g.triples((None, WDT.P31, None)):
        label = next(g.triples(((URIRef(s), RDFS.label, None))), ('_', '_', 'unknown'))[2]
        match(o):
            case WD.Q20667393:
                raceList.append(str(label))
            case WD.Q15632617:
                charList.append(str(label))
            case WD.Q14623646:
                orgList.append(str(label))
            case WD.Q15796005:
                locList.append(str(label))
            case _:
                continue

    return raceList, charList, orgList, locList

def returnList(selection, raceList, charList, orgList, locList):
    match selection:
        case 'Race':
            return raceList
        case 'Character':
            return charList
        case 'Organisation':
            return orgList
        case 'Location':
            return locList

def labelToURL(label):
    url = next(g.triples((None, RDFS.label, Literal(label))), ('_', '_', 'unknown'))[0]
    return url

def createGraph(selection, g):
    config = Config(height=400, width=700)
    selLabel = next(g.triples((URIRef(selection), RDFS.label, None)), ('_','_','unknown'))[2]

    nodes, edges, seen_nodes = [], [], []
    nodes.append(Node(id=str(selection), label=str(selLabel)))
    for _, _, related in g.triples((URIRef(selection), DC.related, None)):
        if related not in seen_nodes:
            relLabel = next(g.triples((URIRef(related), RDFS.label, None)), ('_','_','unknown'))[2]
            nodes.append(Node(id=str(related), label=str(relLabel)))
            seen_nodes.append(related)
        edges.append(Edge(source=str(related), target=str(selection)))


    graphDetails = [nodes, edges, config]
    return graphDetails


g = Graph()
g.parse("results/expandedFiltered.ttl", format="turtle")

baseURL = "https://www.fhgr.ch/master/KE/2024/"
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

rL, cL, oL, lL = generateLists(g)


st.text("Enzyclopeida of Warhammer 40k")
typeDropdown = st.selectbox("Choose what you are looking for:", options= ["Race", "Character", "Organisation", "Location"], index=0)
selection = st.selectbox("Choose...", options=returnList(typeDropdown, rL, cL, oL, lL), index=0)
url = labelToURL(selection)
graphDetails = createGraph(url, g)
agraph(graphDetails[0], graphDetails[1], config=graphDetails[2])
