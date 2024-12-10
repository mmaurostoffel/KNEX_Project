import requests
import json
import re
import streamlit as st
from rdflib import Graph, URIRef, Namespace, RDFS, Literal
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_modal import Modal

STATIC_LOGO_PATH = "https://static.wikia.nocookie.net/warhammer40k/images/6/6e/Warhammer40k-9e-logo.png/revision/latest?cb=20200524130522"

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

def urlToLabel(url):
    label = next(g.triples((URIRef(url), RDFS.label, None)), ('_', '_', 'unknown'))[2]
    return label

def urlToLink(url):
    label = next(g.triples((URIRef(url), WDT.P856, None)), ('_', '_', 'unknown'))[2]
    return label

def createGraph(selection, g):
    config = Config(height=400, width=700, size =20, font={'color': 'white'},)
    selLabel = next(g.triples((URIRef(selection), RDFS.label, None)), ('_','_','unknown'))[2]
    imgURL = next(g.triples((URIRef(selection), SCHEMA.associatedMedia, None)), ('_', '_', 'unknown'))[2]
    imgURL = getImageFromURL(imgURL, 200)

    nodes, edges, seen_nodes = [], [], []
    nodes.append(Node(id=str(selection), label=str(selLabel), shape='circularImage', imagePadding='10', image= imgURL))
    for _, _, related in g.triples((URIRef(selection), DC.related, None)):
        if related not in seen_nodes:
            relLabel = next(g.triples((URIRef(related), RDFS.label, None)), ('_','_','unknown'))[2]
            imgURL = next(g.triples((URIRef(selection), SCHEMA.associatedMedia, None)), ('_', '_', 'unknown'))[2]
            imgURL = getImageFromURL(imgURL, 200)
            nodes.append(Node(id=str(related), label=str(relLabel), shape='circularImage', imagePadding='10', image= imgURL))
            seen_nodes.append(related)
        edges.append(Edge(source=str(related), target=str(selection)))


    graphDetails = [nodes, edges, config]
    return graphDetails

def getImageFromURL(url, size):
    try:
        imageURL = next(g.triples((URIRef(url), SCHEMA.associatedMedia, None)), ('_', '_', 'unknown'))[2]
        response = requests.get(f"https://warhammer40k.fandom.com/wikia.php?controller=CuratedContent&method=getImage&title=File:{imageURL}")
        imgURL = json.loads(response.content)['url']
        imgURL = re.sub(r"(scale-to-width-down\/)(.*)", "scale-to-width-down/" + str(size), imgURL)
    except:
        imgURL = STATIC_LOGO_PATH
    return imgURL


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


# Beginn Page
if 'nodeClicked' not in st.session_state:
    st.session_state['nodeClicked'] = ""

#Sidebar Title + Logo
st.sidebar.title("Encyclopedia of Warhammer 40k")
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.sidebar.image(STATIC_LOGO_PATH)

# Sidebar Selectors
typeDropdown = st.sidebar.selectbox("Class selector", options= ["Race", "Character", "Organisation", "Location"], index=0)
selection = st.sidebar.selectbox("Item selector", options=returnList(typeDropdown, rL, cL, oL, lL), index=0)
url = labelToURL(selection)
print("Session before if: ",str(st.session_state['nodeClicked']))
if st.session_state['nodeClicked'] != "":
    print("If triggered")
    url = st.session_state['nodeClicked']
    st.session_state['nodeClicked'] = ""
imgURL = getImageFromURL(url, 200)

# Sidebar Modal
modal = Modal("Information Panel", key="demo-modal")

open_modal = st.sidebar.button("Info")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.markdown("""
        # Navigation 
        - Select a Topic to search for in the "Topic selector" on the left.
        - Select a specific object you would like to anaylze in the "Item selector".

        You can also search for items by directly clicking on a node in the graph.
        
        # Visualization
        After selecting your item, on the main page you will see all the known information about the item. 
        This includes a link to the base information onf the Warhammer 40k fandom wiki. 
        """)

#Image Information Panel
col1, col2 = st.columns(2)
with st.container():
    with col1:
        st.image(imgURL)
    with col2:
        st.subheader("Name: "+str(urlToLabel(url)))
        st.markdown("Link to Warhammer Wiki: [link](%s)" % urlToLink(url))

# Graph
with st.container():
    graphDetails = createGraph(url, g)
    url = agraph(graphDetails[0], graphDetails[1], config=graphDetails[2])
    if url:
        print("URL Output nach klick: ", url)
        st.session_state.nodeClicked = url
        st.rerun()
