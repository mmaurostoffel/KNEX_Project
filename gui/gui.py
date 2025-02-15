import requests
import json
import re
import streamlit as st
from rdflib import Graph, URIRef, Namespace, RDFS, Literal
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_modal import Modal
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

STATIC_LOGO_PATH = "https://static.wikia.nocookie.net/warhammer40k/images/6/6e/Warhammer40k-9e-logo.png/revision/latest?cb=20200524130522"
STATIC_TEST_IMAGE = "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png"
MAX_NODE_COUNT = 15

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
    selLabel = urlToLabel(selection)

    imgURL = getImageFromURL(selection, 300, outputAsImage = False)
    #print(imgURL)

    nodes, edges, seen_nodes = [], [], []
    #nodes.append(Node(id=str(selection), label=str(selLabel), shape='circularImage', imagePadding='10', image= imgURL))
    #nodes.append(Node(id=str(selection), label=str(selLabel), shape='circularImage', imagePadding='10', image= STATIC_TEST_IMAGE))
    #nodes.append(Node(id=str(selection), label=str(selLabel), font={'color': 'black', 'size': 20}, node={'color': 'black'}))
    count = 0
    for _, _, related in g.triples((URIRef(selection), DC.related, None)):
        count += 1
        if count < MAX_NODE_COUNT:
            if related not in seen_nodes:
                relLabel = urlToLabel(related)


                imgURL = getImageFromURL(related, 200, outputAsImage = False)

                #nodes.append(Node(id=str(related), label=str(relLabel), shape='circularImage', imagePadding='10', image= imgURL))
                #nodes.append(Node(id=str(related), label=str(relLabel), shape='circularImage', imagePadding='10', image = STATIC_TEST_IMAGE))
                nodes.append(Node(id=str(related), label=str(relLabel), color='lightgray', font={'color': 'black', 'size': 20}))
                seen_nodes.append(related)
            edges.append(Edge(source=str(related), target=str(selection)))
    nodes.append(Node(id=str(selection), label=str(selLabel), color='lightgray', font={'color': 'black', 'size': 20}))

    graphDetails = [nodes, edges, config]
    return graphDetails, count

def getImageFromURL(url, size, outputAsImage = True):
    try:
        imageURL = next(g.triples((URIRef(url), SCHEMA.associatedMedia, None)), ('_', '_', 'unknown'))[2]
        response = requests.get(f"https://warhammer40k.fandom.com/wikia.php?controller=CuratedContent&method=getImage&title=File:{imageURL}")
        imgURL = json.loads(response.content)['url']
        imgURL = re.sub(r"(scale-to-width-down\/)(.*)", "scale-to-width-down/" + str(size), imgURL)
        if outputAsImage:
            imgURL = Image.open(requests.get(imgURL, stream=True).raw)
    except:
        imgURL = STATIC_LOGO_PATH
        if outputAsImage:
            imgURL = Image.open(requests.get(imgURL, stream=True).raw)
    return imgURL

def set_node_clicked(url):
    st.session_state.nodeClicked = url

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

rerunCounter = 0

# Beginn Page
if 'nodeClicked' not in st.session_state:
    st.session_state['nodeClicked'] = ""

# Set Page to wide
st.set_page_config(layout="wide")

#Sidebar Title + Logo
st.sidebar.title("Encyclopedia of Warhammer 40k")
left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.sidebar.image(getImageFromURL(STATIC_LOGO_PATH, 200))

# Sidebar Selectors
typeDropdown = st.sidebar.selectbox("Class selector", options=["Race", "Character", "Organisation", "Location"],index=0)
selection = st.sidebar.selectbox("Item selector", options=returnList(typeDropdown, rL, cL, oL, lL), index=0)
url = labelToURL(selection)

# Check if url needs to be overridden
#rerunCounter += 1
#string = 'counter = ', rerunCounter, ' state = ', st.session_state['nodeClicked']
#st.sidebar.markdown(string)

if st.session_state.nodeClicked != "":
    url = st.session_state.nodeClicked
    st.session_state.nodeClicked = ""


imgURL = getImageFromURL(url, 200)

# Sidebar Expander
with st.sidebar.expander("Info"):
    st.markdown("""
        # Navigation 
        - Select a Topic to search for in the "Topic selector" on the left.
        - Select a specific object you would like to anaylze in the "Item selector".

        You can also search for items by directly clicking on a node in the graph.
        
        # Visualization
        After selecting your item, on the main page you will see all the known information about the item. 
        This includes a link to the base information onf the Warhammer 40k fandom wiki. 
        """)

# Image Information Panel
mainCol1, mainCol2 = st.columns([2, 1])
with mainCol1:
    col1, col2 = st.columns(2)
    with st.container():
        with col1:
            st.image(imgURL)
        with col2:
            st.subheader("Name:")
            st.header(""+str(urlToLabel(url)))
            st.markdown("Link to Warhammer Wiki:")
            st.markdown("[Link](%s)" % urlToLink(url))

    # Graph
    with st.container():
        graphDetails, count = createGraph(url, g)
        st.subheader(f"Displaying {min(MAX_NODE_COUNT, count)} of {count} nodes")
        url = agraph(graphDetails[0], graphDetails[1], config=graphDetails[2])
        if url:
            set_node_clicked(url)
            st.rerun()

with mainCol2:
    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    background-color: rgba(93, 4, 18, 1);
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        st.subheader("Frequently searched")
        with st.container():
            st.subheader("Space Marines")
            col11, col12 = st.columns(2)
            url = labelToURL("Space Marines")
            with col11:
                st.image(getImageFromURL(url, 200))
            with col12:
                st.markdown("Link to Warhammer Wiki:")
                st.markdown("[Link](%s)" % urlToLink(url))
                st.button("Search", key="spaceMarinesButton", on_click=set_node_clicked, args=(url,))

        with st.container():
            st.subheader("Orks")
            col11, col12 = st.columns(2)
            url = labelToURL("Orks")
            with col11:
                st.image(getImageFromURL(url, 200))
            with col12:
                st.markdown("Link to Warhammer Wiki:")
                st.markdown("[Link](%s)" % urlToLink(url))
                st.button("Search", key="orksButton", on_click=set_node_clicked, args=(url,))


        with st.container():
            st.subheader("Chaos Cult")
            col11, col12 = st.columns(2)
            url = labelToURL("Chaos Cult")
            with col11:
                st.image(getImageFromURL(url, 200))
            with col12:
                st.markdown("Link to Warhammer Wiki:")
                st.markdown("[Link](%s)" % urlToLink(url))
                st.button("Search", key="chaosCultButton", on_click=set_node_clicked, args=(url,))

