import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from tests.import_fpl import df_season_team, df_season_players, df_haaland

from speedy_charts.charts import Bar, GroupedBar, StackedBar, HorizontalStackedBar, Line, Scatter
from speedy_charts.palettes import af_categorical


# Bar
bar = Bar(x = 'team_x', y = 'goals_scored', df = df_season_team)

bar.plot(colour_palette=af_categorical[0])

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Grouped Bar
bar = GroupedBar(x = 'team_x', y = ['goals_scored', 'assists', 'yellow_cards', 'red_cards', 'minutes'], df = df_season_team)

bar.plot(colour_palette=af_categorical)

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Stacked Bar
bar = StackedBar(x = 'team_x', y = ['goals_scored', 'assists'], df = df_season_team)

bar.plot(colour_palette=af_categorical)

plt.xticks(rotation=45, ha = 'right')

plt.show()


# Horizontal Stacked Bar
bar = HorizontalStackedBar(x = 'team_x', y = ['goals_scored', 'assists'], df = df_season_team)

bar.plot(colour_palette=af_categorical)

plt.show()


# Line
chart = Line(x = 'GW', y = ['cumulative_goals', 'cumulative_assists'], df = df_haaland)

chart.plot()

plt.show()


# Scatter
chart = Scatter(x = 'minutes', y = 'influence', df = df_season_players, category_column='position', category_list=['GK', 'DEF', 'MID', 'FWD'])

chart.plot()

plt.show()