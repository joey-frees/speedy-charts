import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from matplotlib.colors import to_rgba, ListedColormap
import matplotlib.patches as mpatches
from src.speedy_charts.palettes import af_categorical

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
                f"The column {cat_col} is numeric, please provide a non-numeric categorical column to create colour categories, if you wish to create categories based on the numeric column, add a custom_ranges argument")
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

    def plot(self, x_label = '', y_label = '', title = '', colour_palette = af_categorical, legend = False, legend_loc = 'upper center', legend_plot_area = 'outside', theme = 'fivethirtyeight'):
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
            elif self.category_list is not None and self.custom_ranges is None and self.category_column is not None:
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_categories(self.df, self.category_column, colour_list, self.category_list)
                ax.bar(self.df[self.x], self.df[self.y], color=self.df['colour'])
                handles = [mpatches.Patch(color=category_colours[category], label=category) for category in self.category_list]
                handles = sorted(handles, key=lambda handle: self.category_list.index(handle.get_label()))

            # Create bar chart where category column, custom order and custom numeric ranges is specified
            elif self.category_list is not None and self.custom_ranges is not None and self.category_column is not None:
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_ranges(self.df, self.category_column, colour_list, self.category_list, self.custom_ranges)
                ax.bar(self.df[self.x], self.df[self.y], color=self.df['colour'])
                handles = [mpatches.Patch(color=category_colours[category], label=category) for category in self.category_list]
                handles = sorted(handles, key=lambda handle: self.category_list.index(handle.get_label()))

            else:
                ax.bar(self.df[self.x], self.df[self.y], color=colour_palette[0])

        # Create bar from lists/arrays
        else:
            ax.bar(self.x, self.y, color= colour_palette)

        ax.set_xlabel(xlabel=x_label)
        ax.set_ylabel(ylabel=y_label)
        ax.set_title(label=title)

        plt.subplots_adjust(bottom=0.3)

        # Add legend to plot
        if self.custom_ranges is None and self.category_list is None and self.category_column is None:
            self._legend(legend=legend, legend_loc=legend_loc)

        elif self.custom_ranges is not None and self.category_list is None:
            raise ValueError(
                f"When providing a custom_ranges argument you must also provide a category_list argument to assign names to the ranges"
            )
        else:
            # Apply custom legend where category column has been specified
            if legend_plot_area == 'inside':
                # Place legend inside plot area
                ax.legend(handles=handles, loc=legend_loc)
            else:
                # Place the legend outside the plot area
                if 'upper' not in legend_loc and 'lower' not in legend_loc:
                    ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc=legend_loc, borderaxespad=0)
                else:
                    num_items = len(handles)
                    ax.legend(handles=handles, loc=legend_loc, bbox_to_anchor=(0.5, -0.2), ncol=num_items)

        print('Colour Palette - ', colour_palette)

        return ax


class StackedBar(CreateChart):
    def __init__(self, x, y, df=None):
        super().__init__(x, y, df)

    def plot(self, x_label = '', y_label = '', title = '', colour_palette = af_categorical, legend = True, legend_loc = 'upper center', legend_plot_area = 'outside', theme = 'fivethirtyeight'):
        plt.style.use(theme)
        fig, ax = plt.subplots(layout='constrained')

        # Create stacked bar from df
        if self.df is not None:
            if type(self.y) != list:
                raise ValueError("You need to supply multiple y-axis values in a list to create a stacked bar chart")
            else:
                self.df.set_index(self.x, inplace=True)

                # Initialise bottom array to zero
                bottom = np.zeros(len(self.df))

                # Create chart for each category
                if len(self.y) > len(colour_palette):
                    raise ValueError(f"You have more y-axis values ({len(self.y)}) than colours in the palette ({len(colour_palette)}), please provide a larger palette")
                elif type(colour_palette) != list:
                    raise ValueError("You need to supply a colour palette with more than one value to create a stacked bar chart")
                else:
                    for i, item in enumerate (self.y):
                        ax.bar(self.df.index, self.df[item], bottom=bottom, label=item, color=colour_palette[i])
                        bottom += self.df[item] # update the bottom for the next stack

                ax.set_xlabel(xlabel=x_label)
                ax.set_ylabel(ylabel=y_label)
                self._legend(legend=legend, legend_loc=legend_loc, legend_plot_area=legend_plot_area)
                ax.set_title(label=title)
                self.df.reset_index(inplace=True)

                plt.subplots_adjust(bottom=0.3)

                print('Colour Palette - ', colour_palette)

                return ax
        else:
            raise ValueError("You need to supply a dataframe to create a stacked bar chart")


class HorizontalStackedBar(CreateChart):
    def __init__(self, x, y, df=None):
        super().__init__(x, y, df)

    def plot(self, x_label = '', y_label = '', title = '', colour_palette = af_categorical, legend = True, legend_loc = 'lower center', legend_plot_area = 'outside', theme = 'fivethirtyeight'):
        plt.style.use(theme)
        fig, ax = plt.subplots(layout='constrained')

        # Create stacked bar from df
        if self.df is not None:
            if type(self.y) != list:
                raise ValueError("You need to supply multiple y-axis values in a list to create a stacked bar chart")
            else:
                self.df.set_index(self.x, inplace=True)

                # Initialise bottom array to zero
                left = np.zeros(len(self.df))

                # Create chart for each category
                if len(self.y) > len(colour_palette):
                    raise ValueError(f"You have more y-axis values ({len(self.y)}) than colours in the palette ({len(colour_palette)}), please provide a larger palette")
                elif type(colour_palette) != list:
                    raise ValueError("You need to supply a colour palette with more than one value to create a stacked bar chart")
                else:
                    for i, item in enumerate (self.y):
                        ax.barh(self.df.index, self.df[item], left=left, label=item, color=colour_palette[i])
                        left += self.df[item] # update the bottom for the next stack

                ax.set_xlabel(xlabel=x_label)
                ax.set_ylabel(ylabel=y_label)
                self._legend(legend=legend, legend_loc=legend_loc, legend_plot_area=legend_plot_area)
                ax.set_title(label=title)
                self.df.reset_index(inplace=True)

                print('Colour Palette - ', colour_palette)

                return ax
        else:
            raise ValueError("You need to supply a dataframe to create a Horizontal stacked bar chart")


class GroupedBar(CreateChart):
    def __init__(self, x, y, df=None):
        super().__init__(x, y, df)

    def plot(self, x_label = '', y_label = '', title = '', colour_palette = af_categorical, legend = True, legend_loc = 'upper center', legend_plot_area = 'outside', theme = 'fivethirtyeight'):
        plt.style.use(theme)
        fig, ax = plt.subplots(layout='constrained')

        # Create stacked bar from df
        if self.df is not None:
            if type(self.y) != list:
                raise ValueError("You need to supply multiple y-axis values in a list to create a grouped bar chart")
            else:
                self.df.set_index(self.x, inplace=True)

                # Define label locations and bar width
                x = np.arange(len(self.df.index)) # label locations
                n_groups = len(self.y)
                width = 1 / (n_groups + 1) # Bar widths

                # Create chart for each category
                if len(self.y) > len(colour_palette):
                    raise ValueError(f"You have more y-axis values ({len(self.y)}) than colours in the palette ({len(colour_palette)}), please provide a larger palette")
                elif type(colour_palette) != list:
                    raise ValueError("You need to supply a colour palette with more than one value to create a grouped bar chart")
                else:
                    for i, item in enumerate (self.y):
                        offset = width * i
                        ax.bar(x + offset, self.df[item], width, label=item, color=colour_palette[i])

                    ax.set_xticks((x-(0.5*width)) + ((width*len(self.y))/2), self.df.index)

                ax.set_xlabel(xlabel=x_label)
                ax.set_ylabel(ylabel=y_label)
                self._legend(legend=legend, legend_loc=legend_loc, legend_plot_area=legend_plot_area)
                ax.set_title(label=title)
                self.df.reset_index(inplace=True)

                plt.subplots_adjust(bottom=0.3)

                print('Colour Palette - ', colour_palette)

                return ax
        else:
            raise ValueError("You need to supply a dataframe to create a grouped bar chart")


class Line(CreateChart):
    def __init__(self, x, y, df=None):
        super().__init__(x, y, df)

    def plot(self, x_label = '', y_label = '', title = '', colour_palette= af_categorical, legend = False, legend_loc = 'upper center', legend_plot_area = 'outside', theme = 'fivethirtyeight'):
        plt.style.use(theme)
        fig, ax = plt.subplots(layout='constrained')

        # Create line chart from dataframe
        if self.df is not None:
            if type(self.y) != list:
                ax.plot(self.df[self.x], self.df[self.y], c=colour_palette)
            elif type(self.y) == list:
                for i, item in enumerate(self.y):
                    ax.plot(self.df[self.x], self.df[item], label=item, color=colour_palette[i])

        elif self.df is None and type(self.y) != list:
            ax.plot(self.x, self.y, color=colour_palette)

        ax.set_xlabel(xlabel=x_label)
        ax.set_ylabel(ylabel=y_label)
        ax.set_title(label=title)
        self._legend(legend=legend, legend_loc=legend_loc, legend_plot_area=legend_plot_area)

        print('Colour Palette - ', colour_palette)

        return ax

class Scatter(CreateChart):
    def __init__(self, x, y, df=None, category_column=None, category_list=None, custom_ranges=None):
        super().__init__(x, y, df, category_column, category_list, custom_ranges)

    def plot(self, x_label = '', y_label = '', title = '', colour_palette = af_categorical, legend = True, legend_loc = 'upper center', legend_plot_area = 'outside', theme = 'fivethirtyeight' ):
        plt.style.use(theme)
        fig, ax = plt.subplots(layout='constrained')

        #Create scatter plot from dataframe
        if self.df is not None:

            # Basic Scatter with no category split
            if type(self.y) != list and self.category_column is None:
                ax.scatter(self.df[self.x], self.df[self.y])

            # Scatter plot with category split but without custom order specified
            elif type(self.y) != list and self.category_column is not None and self.category_list is None and len(colour_palette) >= len(self.df[self.category_column].unique()):
                # Create a color map for the categories
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_categories(self.df, self.category_column, colour_list, self.category_list)
                ax.scatter(self.df[self.x], self.df[self.y], c=self.df['colour'])
                handles = [mpatches.Patch(color = category_colours[category], label = category) for category in self.df[self.category_column].unique()]

            # Scatter plot with category split and custom category order specified
            elif self.category_list is not None and self.custom_ranges is None and len(colour_palette) >= len(self.category_list):
            # Create a color map for the categories
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_categories(self.df, self.category_column, colour_list, self.category_list)
                ax.scatter(self.df[self.x], self.df[self.y], c=self.df['colour'])
                handles = [mpatches.Patch(color=category_colours[category], label=category) for category in self.category_list]
                handles = sorted(handles, key=lambda handle: self.category_list.index(handle.get_label()))

            # Scatter plot with category split and custom category order and custom numeric ranges
            elif self.category_list is not None and self.custom_ranges is not None and len(colour_palette) >= (len(self.custom_ranges)-1):
            # Create a color map for the categories
                colour_list = self.convert_hex_list_to_rgba(colour_palette)
                category_colours = self.create_colour_ranges(self.df, self.category_column, colour_list, self.category_list, self.custom_ranges)
                ax.scatter(self.df[self.x], self.df[self.y], c=self.df['colour'])
                handles = [mpatches.Patch(color=category_colours[category], label=category) for category in self.category_list]
                handles = sorted(handles, key=lambda handle: self.category_list.index(handle.get_label()))

            elif self.custom_ranges is not None and self.category_list is None:
                raise ValueError(
                    f"When providing custom ranges, you need to also provide a category list to assign names to the ranges"
                )

            # Raise error if number of colours required is larger than the palette (too many categories)
            else:
                raise ValueError(
                    f" You have more categories ({len(self.df[self.category_column].unique())}) than colours in the palette ({len(colour_palette)}), please provide a larger palette or choose a column with fewer categories"
                )

        # Create scatter with multiple y_axis values specified
        elif type(self.y) == list and self.category_column is None:
            for i, item in enumerate(self.y):
                ax.scatter(self.x, self.y, color= af_categorical)

        elif self.df is None and type(self.y) != list:
            ax.scatter(self.x, self.y, color = af_categorical[0] )

        ax.set_xlabel(xlabel=x_label)
        ax.set_ylabel(ylabel=y_label)
        ax.set_title(label=title)

        # Add legend to plot
        if self.category_column is None:
            self._legend(legend = legend, legend_loc = legend_loc)
        else:
            # Apply custom legend where category column has been specified
            if legend_plot_area == 'inside':
                ax.legend(handles = handles, loc = legend_loc)
            else:
                # Place the legend outside the plot area
                if 'upper' not in legend_loc and 'lower' not in legend_loc:
                    ax.legend(handles = handles, bbox_to_anchor=(1.05, 1), loc=legend_loc, borderaxespad=0)

                else:
                    num_items = len(handles)
                    ax.legend(handles = handles, loc = legend_loc, bbox_to_anchor=(0.5, -0.2), ncol=num_items)

        print('Colour Palette - ', colour_palette)

        return ax