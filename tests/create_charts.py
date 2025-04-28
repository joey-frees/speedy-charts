import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from tests.import_fpl import df_season_team, df_season_players, df_haaland

from speedy_charts.charts import Bar, GroupedBar, StackedBar, HorizontalStackedBar, Line, Scatter
from speedy_charts.palettes import af_categorical


# Simple Bar
bar = Bar(x = 'team_x', y = 'goals_scored', df = df_season_team)

bar.plot(title= 'Goals by team', x_label='Team', y_label='Goals')

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Bar Ranges
chart = Bar(x = 'team_x', y = 'goals_scored', df = df_season_team, category_column='goals_scored', category_list=['low', 'medium', 'high'], custom_ranges=[0,50,75,float('inf')])

chart.plot(x_label='Team', y_label='Goals', title='Goals by team')

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Grouped Bar
chart = GroupedBar(x = 'team_x', y = ['goals_scored', 'assists', 'yellow_cards'], df = df_season_team)

chart.plot(colour_palette=af_categorical, title='Stats by Team', x_label='Team', y_label='Goals/Assists/Yellow Cards', legend=True)

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Stacked Bar
chart = StackedBar(x = 'team_x', y = ['goals_scored', 'assists', 'yellow_cards'], df = df_season_team)

chart.plot(colour_palette=af_categorical, title='Stats by Team', x_label='Team', y_label='Goals/Assists/Yellow Cards', legend=True)

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Horizontal Stacked Bar
chart = HorizontalStackedBar(x = 'team_x', y = ['goals_scored', 'assists', 'yellow_cards'], df = df_season_team)

chart.plot(colour_palette=af_categorical, title='Stats by Team', x_label='Goals/Assists/Yellow Cards', y_label='Team', legend=True)

plt.show()


# Line
chart = Line(x = 'GW', y = ['cumulative_goals', 'cumulative_assists'], df = df_haaland)

chart.plot(title='Haaland - Cumulative goals/assists', x_label='GW', y_label='Goals/Assists', legend=True)

plt.show()


# Scatter
chart = Scatter(x = 'minutes', y = 'influence', df = df_season_players)

chart.plot(title='Influence by average minutes', x_label='Mean Minutes', y_label='Mean Influence')

plt.show()


# Scatter Categories
chart = Scatter(x = 'minutes', y = 'influence', df = df_season_players, category_column='position', category_list=['GK', 'DEF', 'MID', 'FWD'])

chart.plot(title='Influence by average minutes split by position', x_label='Mean Minutes', y_label='Mean Influence')

plt.show()


# Scatter Ranges
chart = Scatter(x = 'minutes', y = 'influence', df = df_season_players, category_column='influence', category_list=['Low', 'Medium', 'High', 'Very High'], custom_ranges=[0, 10, 20, 30, float('inf')])

chart.plot(colour_palette=['#A1DAB4', '#41B6C4', '#2C7FB8', '#003479'], title='Influence by average minutes split by position', x_label='Mean Minutes', y_label='Mean Influence')

plt.show()