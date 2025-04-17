import pandas as pd

df = pd.read_csv(r"C:\Users\joefr\Documents\FPL Data\cleaned_merged_seasons.csv", low_memory=False)

df_season = df[df['season_x'] == '2023-24']

df_season_team = df_season.groupby('team_x').agg({
    'goals_scored': 'sum',
    'assists': 'sum',
    'yellow_cards': 'sum',
    'red_cards': 'sum',
    'minutes': 'mean'
}).reset_index()

df_season_players = df_season.groupby('name').agg({
    'position':'first',
    'goals_scored': 'sum',
    'assists': 'sum',
    'yellow_cards': 'sum',
    'red_cards': 'sum',
    'minutes': 'mean',
    'creativity': 'mean',
    'influence': 'mean'
}).reset_index()

df_haaland = df_season[df_season['name'] == 'Erling Haaland']

df_haaland = df_haaland.copy()

df_haaland.loc[:,'cumulative_goals'] = df_haaland['goals_scored'].cumsum()

df_haaland.loc[:,'cumulative_assists'] = df_haaland['assists'].cumsum()








