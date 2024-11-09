import pandas as pd

path = "../dok/fandomData.csv"
df = pd.read_csv(path)
print(df.head())