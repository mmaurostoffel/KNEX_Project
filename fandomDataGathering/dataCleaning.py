import pandas as pd
import re

def removeFile(text):
    stop = False
    while not stop:
        match = re.search(r'\[\[File:', text)
        if match:
            count = 2
            charNum = 0
            searchStart = match.start()
            searchEnd = searchStart + 200
            searchText = text[match.start():searchEnd]
            for char in searchText:
                charNum += 1
                if char == "[":
                    count += 1
                if char == "]":
                    count -= 1
                if count == 0:
                    break

            fileEnd = searchStart + charNum
            text = text[:searchStart] + text[fileEnd:]
        else:
            return text


path = "../dok/fandomData.csv"
df = pd.read_csv(path)


cleanText = []
for _, row in df.iterrows():
    text = row['text']
    #print(text)
    #Alle Anhänge entfernen
    text = re.sub(r'==Sources==.*', '', text, flags=re.DOTALL)
    #Alle File: Instanzen entfernen
    text = removeFile(text)
    #Alle restlichen Sonderzeichen entfernen
    text = re.sub(r'[\<\>\"\'\*\[\]\{\}\(\)/\\\n\t=\-\–\|]', ' ', text)
    #Alle entstandenen Doppelabstände durch Einzelabstände ersetzen
    text = re.sub(r'  ', ' ', text)
    cleanText.append(text)


df['cleanText'] = cleanText
df.to_csv("../dok/fandomDataCleaned.csv", index=False)



#Step 1
#Remove [[File:...]]


#Remove bold, kursiv '
#Remove Quote {{, }}
#Remove Links [[, ]]
#Remove /n, /t,
#Remove Quotations "
#Remove title marks =
#Remove misc *, -