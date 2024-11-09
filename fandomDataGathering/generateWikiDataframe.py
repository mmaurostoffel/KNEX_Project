import os
import xml.etree.ElementTree as ET
import pandas as pd

def extractInfosFromPages(file_path):

    ns = '{http://www.mediawiki.org/xml/export-0.11/}'


    tree = ET.parse(file_path)
    root = tree.getroot()
    title = root.find(ns+'title')

    rev = root.find(ns+'revision')
    id = rev.find(ns+'id')
    text = rev.find(ns+'text')

    baselink = "https://warhammer40k.fandom.com/wiki/"
    link = baselink + (title.text.replace(" ", "_"))

    return title.text, id.text, link, text.text




pageLocations = "../dok/splitFiles"

first = True
fullList = []

numOfFiles = 85485
counter = 1
for filename in os.listdir(pageLocations):

    title, id, link, text = extractInfosFromPages(pageLocations +"/"+filename)

    # Alle pages mit einem ":" im Titel werden ignoriert, da es sich dabei um
    # spezielle Dateien handelt und nicht um tasächliche Inhalte
    if ":" not in title:
        if text:
            if len(text) > 100:
                fullList.append([title, id, link, text])

    if counter % 100 == 0:
        print(str(counter) + " / " + str(numOfFiles))
    counter += 1

df = pd.DataFrame(fullList, columns = ['title', 'id', 'link', 'text'])
df.to_csv("../dok/fandomData.csv", index=False)

    