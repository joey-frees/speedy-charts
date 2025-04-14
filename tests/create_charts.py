import pandas as pd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


from speedy_charts.charts import Bar, GroupedBar, StackedBar, HorizontalStackedBar, Line, Scatter

from speedy_charts.palettes import af_categorical

df = pd.read_csv(r"C:\Users\joefr\Documents\FPL Data\cleaned_merged_seasons.csv", low_memory=False)

df_season = df[df['season_x'] == '2023-24']

df_season_team = df_season.groupby('team_x').agg({
    'goals_scored': 'sum',
    'assists': 'sum',
    'yellow_cards': 'sum',
    'red_cards': 'sum'
}).reset_index()

df_season_players = df_season.groupby('name').agg({
    'goals_scored': 'sum',
    'assists': 'sum',
    'yellow_cards': 'sum',
    'red_cards': 'sum',
    'minutes': 'mean',
    'creativity': 'mean',
    'influence': 'mean'
}).reset_index()



bar = Bar(x = 'team_x', y = 'goals_scored', df = df_season_team)

bar.plot(colour_palette=af_categorical[0])

plt.xticks(rotation=45, ha = 'right')

plt.show()