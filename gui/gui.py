import streamlit as st
from rdflib import Graph, URIRef, Namespace
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore


def generateLists(g):
    raceList, charList, orgList, locList = [],[],[],[]

    for s, _, _ in g.triples((None, WDT.P31, WD.Q20667393)):
        raceList.append(str(s))
    for s, _, name in g.triples((None, WDT.P31, WD.Q15632617)):
        charList.append(s)
    for s, _, name in g.triples((None, WDT.P31, WD.Q14623646)):
        orgList.append(s)
    for s, _, name in g.triples((None, WDT.P31, WD.Q15796005)):
        locList.append(s)

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
def createGraph(selection, g):
    config = Config(height=600, width=760)
    # Retrieve page URL
    print(selection)
    currPage =""
    for _,_, page in g.triples((selection, WDT.P856, None)):
        currPage = page
        print("PAGE: ", str(page))
        break

    nodes, edges, seen_nodes = [], [], []
    for related, _, _ in g.triples((None, WDT.P856, currPage)):
        print("RELATED: ",str(related))
        if related not in seen_nodes:
            nodes.append(Node(id=str(related)))
            seen_nodes.append(related)
        edges.append(Edge(source=str(related), label="dc:related", target=str(currPage)))


    graphDetails = [nodes, edges, config]
    return graphDetails





g = Graph()
g.parse("results/fullTripleStore_expanded.ttl", format="turtle")

baseURL = "https://www.fhgr.ch/master/KE/2024/"
WDT = Namespace("http://www.wikidata.org/prop/direct/")
WD = Namespace("http://www.wikidata.org/entity/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
g.bind("wdt", WDT)
g.bind("wd", WD)
g.bind("dc", DC)

g2 = Graph()
nodeWithPage = []
# Vorfiltern
# alle Nodes mit Files auswählen
for s, o, p in g.triples((None, WDT.P856, None)):
    nodeWithPage.append(s)

# Alle Inhalte aller Nodes mit Files in neuen TripleStore aufnehmen
for s, o, p in g.triples((None, None, None)):
    if s in nodeWithPage:
        g2.add((s, o, p))

# Overwrite g
g = g2
rL, cL, oL, lL = generateLists(g)


st.text("Enzyclopeida of Warhammer 40k")
typeDropdown = st.selectbox("Choose what you are looking for:", options= ["Race", "Character", "Organisation", "Location"], index=0)
selection = st.selectbox("Choose...", options=returnList(typeDropdown, rL, cL, oL, lL), index=0)

graphDetails = createGraph(selection, g)
print(graphDetails)
agraph(graphDetails[0], graphDetails[1], config=graphDetails[2])
