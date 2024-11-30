import pandas as pd


df = pd.read_csv("../results/mergedEntityList_fuzzy.csv")

nonDupeRows = df[df.duplicated(subset=['Wiki_entity']) == False]

dupeRows = df[df.duplicated(subset=['Wiki_entity']) == True]


max_ratios  = dupeRows.groupby(['Wiki_entity']).ratio.max().reset_index()


bestDupeRows = pd.merge(df, max_ratios, on=['Wiki_entity', 'ratio'], how='inner')
bestDupeRows = bestDupeRows.drop_duplicates(subset=['Wiki_entity'])

filteredFuzzyMerged = pd.concat([nonDupeRows, bestDupeRows])
filteredFuzzyMerged = filteredFuzzyMerged.drop_duplicates(subset=['Wiki_entity'])

filteredFuzzyMerged = filteredFuzzyMerged.drop_duplicates(subset=['Wiki_clean_entities'])

filteredFuzzyMerged.to_csv("../results/mergedEntityList_fuzzy_filtered.csv", index=False)


