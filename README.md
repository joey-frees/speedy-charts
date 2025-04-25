# speedy-charts

## Description
This package is designed to make simple plotting easier, applying a logical syntax to a matplotlib backend!

The following chart types are supported: Bar, Line, Scatter, Stacked Bar, Horizontal Stacked Bar, Grouped Bar

## Installation
To install the package, run the following code in the terminal:
```terminal
pip install 
```
Or run an equivalent command for your package manager of choice, for example in poetry:
```terminal 
poetry add
```

## Usage
### Importing the package
To use the package you should use the following import statements at the top of your script:

```python
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from speedy_charts.charts import Bar, Scatter, StackedBar, HorizontalStackedBar, GroupedBar, Line
from speedy_charts.palettes import af_categorical
```

You can choose to only specify the charts and palettes htat you need for your specific task.

The ```matplotlib.use('TkAgg')``` ensures that the plots can be displayed interactively.

### General usage guidance
The package syntax is based around two elements:
1. The chart object - here, you specify arguments relating to the data that goes into the chart
2. The plot method - here, you specify arguments relating to the visual aspects of the chart

The chart object for example, contains arguments relating to the dataframe you are plotting from, x/y axis values and categorisation if applicable.

The plot method on the other hand, contains arguments relating to colour palette, title, x/y axis labels and legend.

You can also apply any additional transformations to the chart that aren't included in the plot method using standard matplotlib pyplot methods.

**__Please note, you can recreate all of the dataframes used in the example code by running the code in '[Dataframes for chart examples](...)' section below.__**

### Bar
#### Basic Bar
For a basic bar chart, you need to provide, x and y axis values and the dataframe in the chart object.

All other arguments, including those in the plot method are optional, however axis labels and a title are recommended at a minimum.

```python

```

<img src="assets/basic_bar.png" alt="Description" width="800" height="480">

This code creates a basic bar chart, but also includes a transformation using a standard matplotlib method 'xticks' to rotate the x-axis labels.


#### Applying categorical colours
You can also add category arguments to a standard bar chart to colour the bars by a categorical or numeric variable:
* If using a categorical column, this can be achieved by providing the 'category_column' arguments
* If using a numeric column, this can be achieved by providing the 'category_column', 'category_list' and 'custom_ranges' arguments

```python

```

<img src="assests/bar.png" alt="Description" width="800" height="480">


In this example, the 'custom_ranges' argument specifies the ranges of the category_column that the colours will correspond to and the 'category_list' argument provides names for the ranges.
Please note that the 'category_list' is always one element smaller than the 'custom_ranges', list.

### Grouped Bar
A grouped bar chart takes the same arguments as a standard bar chart but requires multiple y-axis values passed as a list.

```python

```

<img src="assests/grouped_bar.png" alt="Description" width="800" height="480">

### Stacked Bar
A stacked bar chart takes the same arguments as a standard bar chart but requires multiple y-axis values passed as a list, similar to the grouped bar.

```python

```

<img src="assests/stacked_bar.png" alt="Description" width="800" height="480">

### Horizontal Stacked Bar
A horizontal stacked bar chart takes the same arguments as a standard bar chart but requires multiple y-axis values passed as a list, similar to the grouped bar and stacked bar.

```python

```

<img src="assests/horizontal_bar.png" alt="Description" width="800" height="480">

### Line
The code for producing a line chart also follows the structure of the standard bar and alternative bar charts.
If you are creating a line chart with multiple lines you can supp;ly multiple y-axis values as a list.

```python

```

<img src="assests/line.png" alt="Description" width="800" height="480">

### Scatter
For a basic scatter plot the syntax is very similar to any other plot with x and y-axis values and a dataframe supplied in the initial chart object and the visual options defined in the plot method
To add in categorical colours to the plot you will need to supply a category column argument. In this example an optional 'category list' argument is also supplied to re-order the categories and an alternative colour palette specified.

```python

```

<img src="assests/scatter.png" alt="Description" width="800" height="480">

Similar to the bar chart you can add in custom ranges to the scatter plot by providing the 'category_list' and 'custom_ranges' arguments. The custom ranges are defined in the same way as the bar chart.
In addition, there is an alternative colour palette applied to the scatter

```python

```

<img src="assests/scatter_ranges.png" alt="Description" width="800" height="480">

### Colour Palettes
This package also includes a number of colour palettes that can be used in the plot method. The default palette consists of categorical colours.
You can define the colour palette you want to use by specifying the 'colour_palette' argument in the plot method.

These are defined in the palettes.py file and include:
* af_categorical - a categorical colour palette with the standard analysis function colours
* std_sequential_5/7/9 - a sequential colour palette with 5, 7 or 9 colours
* oth_sequential_5/7/9 - a sequential colour palette with 5, 7 or 9 alternative colours
* std_diverging_5/7/9 - a diverging colour palette with 5, 7 or 9 colours
* oth_diverging_5/7/9 - a diverging colour palette with 5, 7 or 9 alternative colours

You can also pass a custom colour palette to a chart by supplying a list of hex codes

```python

```

<img src="assests/scatter_palette.png" alt="Description" width="800" height="480">

### Themes
Standard styling is applied to the package by default, but you can also apply a custom theme to the chart by using the 'theme' argument in the plot method.
You can use standard matplotlib themes, pre-defined mplstyles, or create your own.

Below is an example of how to apply an inbuilt matplotlib style:

<img src="assests/scatter_ggplot.png" alt="Description" width="800" height="480">

To apply a custom theme using an mplstyle you would structure your theme argument as follows:

```python
chart.lot(theme= 'speedy_charts.mplstyles.custom_theme')
```

## Dataframes for chart examples
All example charts can be created using the following dataframes. You need to initialise these for the example code to work.

```python

```

```python

```

```python

```

```python

```

## Support
If you have any queries regarding hte package and its usage, please contact me.

## Roadmap
* Histogram, pie boxplot and heatap charts as well as additional charting options to be added to the package
* Additional custom themes to be added

## Contributing
For any ideas on how the package could be improved, or if you find any bugs, please contact me.