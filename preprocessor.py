import pandas as pd


def preprocess(df,region_df):
  # global df, region_df

# Filterin for summer olympics
  df = df[df['Season'] == 'Summer']

# Merge with region_df
  df = df.merge(region_df, on='NOC',how='left')

# Dropping Duplicates 
  df.drop_duplicates(inplace=True)

  df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
  return df