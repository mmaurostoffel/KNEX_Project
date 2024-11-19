import pandas as pd

#path = "../dok/fandomData.csv"
#path = "../dok/fandomData_NER_withWikiSyntax.csv"
#path = "../dok/fandomDataCleaned.csv"
path = "../dok/fandomData_NER_withSpacy.csv"
df = pd.read_csv(path)
print(df.head())