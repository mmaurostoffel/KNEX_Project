import pandas as pd
df1 = pd.read_csv("../dok/old/fandomData_NER_withSpacy_smallBackup.csv")
df2 = pd.read_csv("../dok/old/fandomData_NER_withSpacy.csv")

df = pd.merge(df1, df2, on='title', how='left')
df = df[['title', 'id_x', 'link_x', 'text_x', 'cleanText_x', 'named_entities_y']]
df = df.rename(columns={'id_x':'id', 'link_x':'link', 'text_x':'text', 'cleanText_x':'cleanText', 'named_entities_y':'named_entities'})
print(df)
df.to_csv("../dok/fandomData_NER_withSpacy.csv", index=False)