import numpy as np

def medal_tally(df):
  medal_tally = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
  medal_tally = medal_tally.groupby('NOC').sum()[["Gold","Silver","Bronze"]].sort_values('Gold',ascending=False).reset_index()

  medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']


  return medal_tally


def country_year_list(df):
  years = df['Year'].unique().tolist()
  years.sort()
  years.insert(0,'Overall')

  country = df['region'].dropna().unique().tolist()
  country.sort()
  country.insert(0,'Overall')

  return years,country

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        X = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending= True).reset_index()
    else:
        X = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending= False).reset_index()
    X['Total'] = X['Gold'] + X['Silver'] + X['Bronze']
    return(X)


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns= {'Year': 'Edition','count': col},inplace=True)
    return nations_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=["Medal"])
    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset="Medal")
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"],inplace=True)
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset="Medal")
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"],inplace=True)
    new_df = temp_df[temp_df['region']==country]
    pt = new_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc="count").fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    return x

def weight_v_height(df,sport):
    athelete_df = df.drop_duplicates(subset=["Name","region"])
    athelete_df["Medal"].fillna("No Medal",inplace=True)
    if sport != "Overall":
         temp_df = athelete_df[athelete_df["Sport"] == sport]
         return temp_df
    else:
        return athelete_df
    
def men_v_women(df):
    athelete_df = df.drop_duplicates(subset=["Name","region"])
    men = athelete_df[athelete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index()
    women = athelete_df[athelete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index()
    final = men.merge(women,on="Year",how="left")
    final.rename(columns={"Name_x":"Male","Name_y":"Female"},inplace=True)
    final.fillna(0,inplace=True)

    return final


