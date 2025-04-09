import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from matplotlib.colors import to_rgba, ListedColormap
import matplotlib.patches as mpatches

class CreateChart:
    def __init__(self, x, y, df = None, category_column = None, category_list = None, custom_ranges = None):
        self.df = df
        self.x = x
        self.y = y
        self.category_column = category_column
        self.category_list = category_list
        self.custom_ranges = custom_ranges

    def _legend(self, legend = False, legend_loc = 'upper right', legend_plot_area = 'outside'):
        if legend:
            if type(self.y) != list:
                pass
            else:
                if legend_plot_area == 'inside':
                    plt.legend(loc=legend_loc)
                else:
                    if 'upper' not in legend_loc and 'lower' not in legend_loc:
                        plt.legend(bbox_to_anchor=(1.05, 1), loc=legend_loc, borderaxespad=0)
                    else:
                        num_items = len(plt.gca().get_legend_handles_labels()[1])
                        plt.legend(loc=legend_loc, bbox_to_anchor=(0.5, -0.2), ncol=num_items)
        else:
            pass

    @staticmethod
    def convert_hex_list_to_rgba(hex_list):
        return [to_rgba(hex) for hex in hex_list]

    def create_colour_categories(self, df, cat_col, colours, category_list = None):
        if pd.api.types.is_numeric_dtype(df[cat_col]) is True:
            raise ValueError(
                f"The column {cat_col} is numeric, please provide a non-numeric categorical column to create colour categories, if you wish to create categories based on the numeric column, add a custom_ranges argument"
            )
        else:
            colour_list = self.convert_hex_list_to_rgba(colours)
            cmap = ListedColormap(colour_list)

            # Map categories to colours
            if cat_col is not None and category_list is None:
                category_colours = {category: cmap(i) for i, category in enumerate(df[cat_col].unique())}
                df.loc[:, 'colour'] = df[cat_col].map(category_colours)
                return category_colours
            elif category_list is not None:
                category_colours = {category: cmap(i) for i, category in enumerate(category_list)}
                df.loc[:, 'colour'] = df[cat_col].map(category_colours)
                return category_colours

    def create_colour_ranges(self, df, cat_col, colours, category_order = None, custom_ranges = None):
        if pd.api.types.is_numeric_dtype(df[cat_col]) is False:
            raise ValueError(
                f"The column {cat_col} is categorical, a custom_ranges argument is not required. If you want to assign colours based on ranges - please provide a numeric column"
            )
        colour_list = self.convert_hex_list_to_rgba(colours)
        cmap = ListedColormap(colour_list)

        # Map ranges to colours
        if len (category_order) != len(custom_ranges)-1:
            raise ValueError(
                f"When providing custom ranges, the number of categories ({len(category_order)}) must be one less than the number of ranges ({len(custom_ranges)}). Add 'float('inf')' to the end of the ranges to include all values above the last range i.e. 'custom_ranges=[0,10,20, float('inf')]'"
            )
        else:
            df['range_category'] = pd.cut(df[cat_col], bins=custom_ranges, labels=category_order, right=False)
            df['range_category'] = df['range_category'].astype(str)
            category_colours = {category: cmap(i) for i, category in enumerate(category_order)}
            df.loc[:,'colour'] = df['range_category'].map(category_colours)

        return category_colours

class Bar(CreateChart):
    def __init__(self, x, y, df = None, category_column = None, category_list = None, custom_ranges = None):
        super().__init__(x, y, df, category_column, category_list, custom_ranges)

    def plot(self, x_label = '', y_label = '', title = '', colour_palette = , legend = False, legend_loc = 'lower center', legend_plot_area = 'outside', theme = ):
        plt.style.use(theme)
        fig, ax = plt.subplots(layout = 'constrained')

        if self.df is not None:

            # Create bar chart where category column is specified
            if self.category_list is None and self.custom_ranges is None and self.category_column is not None:
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_categories(self.df, self.category_column, colour_list, list(self.df[self.category_column].unique()))
                ax.bar(self.df[self.x], self.df[self.y], color=self.df['colour'])
                handles = [mpatches.Patch(color=category_colours[category], label=category) for category in list(self.df[self.category_column].unique())]
                handles = sorted(handles, key=lambda handle: list(self.df[self.category_column].unique()).index(handle.get_label()))

            # Create bar chart where category column and a custom order is specified
            if self.category_list is not None and self.custom_ranges is None and self.category_column is not None:
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_categories(self.df, self.category_column, colour_list, self.category_list)
                ax.bar(self.df[self.x], self.df[self.y], color=self.df['colour'])
                handles = [mpatches.Patch(color=category_colours[category], label=category) for category in self.category_list]
                handles = sorted(handles, key=lambda handle: self.category_list.index(handle.get_label()))

