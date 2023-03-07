import typing as t
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
BLUE, RED = "#4389E3", "#CC2F4A"
LIGHT_BLUE, LIGHT_RED = "#CBCFDC", "#DEB3B3"
COLORS_D = ["#86B6F2", "#4389E3", "#1666CB", "#0645B4", "#002B84"]
COLORS_R = ["#E27F90", "#CC2F4A", "#D40000", "#AA0000", "#800000"]
COLOR_GREY = "#D6D6D6"
YEARS = [f"{i}" for i in range(2000, 2024, 4)]
JSON = t.Union[str, int, float, bool, None,
               t.Mapping[str, 'JSON'], t.List['JSON']]


def draw_map(geojson: JSON,
             data: pd.DataFrame,
             location_column: str,
             color_column: str,
             map_name: str) -> None:
    """Draws a map of Texas using the data provided.

    Args:
        geojson (JSON): the GEOJSON object used to draw the map.
        data (pd.DataFrame): a DataFrame containing the data,
            columns must contain location_column and color_column.
        location_column (str): the name of the column containing
            the code of the subdivision (county/state).
        color_column (str): the name of the column containing
            the colors to be drawn.
        map_name (str): the name of the.
    """ 
    color_map = {i: i for i in COLORS_D+COLORS_R+[COLOR_GREY]}
    fig = px.choropleth_mapbox(data,
                               geojson=geojson,
                               locations=location_column,
                               color=color_column,
                               color_discrete_map=color_map,
                               range_color=(-100, 100),
                               mapbox_style="white-bg",
                               zoom=5.75,
                               center={"lat": 31.3915, "lon": -99.7707})
    fig.update_layout(margin={"r": 0,
                              "t": 0,
                              "l": 0,
                              "b": 0})
    fig.update_traces(marker_line_color="white",
                      marker_line_width=2,
                      showlegend=False)
    fig.write_image(map_name, width=1200, height=1200)


def draw_bar_chart(y: t.List[str],
                   values: t.List[t.List[float]],
                   colors: t.List[t.List[str]],
                   ax: plt.Axes) -> plt.Axes:
    """Draws a stacked horizontal barchart.

    Args:
        y (t.List[str]): the names of the y-labels.
        values (t.List[t.List[float]]): the values to be drawn, should
            be of the same shape as the colors.
        colors (t.List[t.List[str]])): the colors.
        ax (plt.Axes): the axes to be plotted on.

    Returns:
        The axes containing the resulting bar chart.
    """ 
    plots = []
    for i, (values_, colors_) in enumerate(zip(values, colors)):
        if i:
            plot = ax.barh(y, values_, color=colors_,
                           left=values[i-1])
        else:
            plot = ax.barh(y, values_, color=colors_)
        plots += [plot]
    return ax


def add_annot(text: str,
              patch_number: int,
              ax: plt.Axes,
              **kwargs) -> plt.Axes:
    """Adds annotation to the axes containing the bar chart.

    Args:
        text (str): the text of the annotation.
        patch_number (int): the number of the patch. In this case,
            0 represents the left patch of the first row, while
            11 represents the right patch of the last row.
        ax (plt.Axes): the axis to be plotted on.
        kwargs: keyword arguments passed to ax.text().

    Returns:
        The axes containing the annotation.
    """
    patch = ax.patches[patch_number]
    width, height = patch.get_width(), patch.get_height()
    x, y = patch.get_xy()
    ax.text(x+width/2,
            y+height/2,
            text,
            ha="center",
            va="center",
            **kwargs)
    return ax


def create_chart(values: t.List[t.List[float]],
                 row_number: int,
                 name: str) -> None:
    """Draws and edits a stacked horizontal barchart.

    Args:
        values (t.List[t.List[float]]): the values to be drawn.
        row_number (int): the number of the row to be highlighted
            and annottated. Should be in [0; 5].
        name (str): the name of the chart.
    """
    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    colors = [[LIGHT_BLUE]*6, [LIGHT_RED]*6]
    for i in range(2):
        colors[i][row_number] = [BLUE, RED][i]
    ax = draw_bar_chart(YEARS, values, colors, ax)
    ax = add_annot(f"   {round(values[0][row_number], 2)}%", row_number, ax,
                   size = 17, fontfamily="Roboto")
    ax = add_annot(f"   {round(values[1][row_number], 2)}%", row_number+6, ax,
                   size = 17, fontfamily="Roboto")
    for i in ["top", "right", "left", "bottom"]:
        ax.spines[i].set_visible(False)
    ax.tick_params(axis="both", which="major", length=0,
                   labelsize=17)
    ax.set_xticks([])
    ax.margins(x=0, y=0)
    ax.invert_yaxis()
    ax.yaxis.tick_right()
    plt.savefig(name)
    ax.cla()

    
if __name__ == "__main__":
    main()
            
    
    
