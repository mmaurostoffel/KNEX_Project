import pandas as pd
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

#path = "../dok/fandomData.csv"
#path = "../dok/fandomData_NER_withWikiSyntax.csv"
#path = "../dok/fandomDataCleaned.csv"
#path = "../dok/fandomData_NER_withSpacy.csv"
#path = "../dok/fandomData_NER_withSpacy_smallBackup.csv"


df = pd.read_csv(filename)
print(df.head())