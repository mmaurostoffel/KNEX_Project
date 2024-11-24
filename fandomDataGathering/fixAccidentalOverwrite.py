import pandas as pd

path1 = "../dok/old/fandomData_NER_withSpacy.csv"
df1 = pd.read_csv(path1)
print(df1.head(10))

df = df1.assign(named_entities='')
mask = (df['cleanText'].str.len() > 100)
df = df.loc[mask]

print(df.head(10))
df.to_csv("../dok/fandomData_NER_withSpacy.csv")