import typing as t
import imageio
import json
import os
import PIL
from PIL import ImageDraw, ImageFont
JSON = t.Union[str, int, float, bool, None,
               t.Mapping[str, 'JSON'], t.List['JSON']]
COLORS_D = ["#86B6F2", "#4389E3", "#1666CB", "#0645B4", "#002B84"]
COLORS_R = ["#E27F90", "#CC2F4A", "#D40000", "#AA0000", "#800000"]
COLOR_GREY = "#D6D6D6"
THRESH_MARGIN = [50, 60, 70, 80, 90, 100]


def get_color(value: float,
              thresh: t.List[float]=THRESH_MARGIN) -> str:
    """Transforms the value into the corresponding color.

    Args:
        value (float): the value to be transformed.
        thresh (t.List[float]): the list of threshold values,
            defaults to THRESH_MARGIN.

    Returns:
        The color from COLORS_D or COLORS_R, corresponding to the value, with
        the color palette determined by whether the value is negative or
        positive: COLORS_D for negative values, COLORS_R for positive ones.

    Examples:
        >>> print(get_color(51.3))
        '#E27F90'

        >>> print(get_color(-65.7))
        '#4389E3'
    """
    colors = COLORS_D if value < 0 else COLORS_R
    for i, (left, right) in enumerate(zip(thresh, thresh[1:])):
        if left < abs(value) <= right:
            return colors[i]
    if value > thresh[-1]:
        return colors[-1]
    

def read_json(path: str) -> JSON:
    """Reads .json file from a file path.

    Args:
        path (str): a file path.

    Returns:
        A JSON object, represented as a dict.
    """
    with open(path) as json_file:
        return json.load(json_file)


def grey_out(name: str,
             color: str,
             colored_name: str,
             color_grey: str=COLOR_GREY) -> str:
    """Turns the subdivision's color to grey if it should be greyed out.

    Args:
        name (str): the name of the subdivision.
        color (str): the color to be used.
        colored_name (str): the name of the subdivision that should be colored.
        color_grey (str): the grey color used. Defaults to COLOR_GREY.

    Returns:
        Color, if the subdivision should not be greyed out;
        otherwise, color_grey.
    """
    return color if name == colored_name else color_grey

    
def make_gif(file_names: t.List[str],
             gif_name: str,
             frame_duration: float=1,
             delete_files: bool=True) -> None:
    """Creates a gif from a list of images.

    Args:
        file_names (t.List[str]): the list of names of the images.
        gif_name (str): the name of the resulting gif.
        frame_duration (float): the duration of each frame, defaults to 1.
        delete_files (bool): whether the delete the original files,
            defaults to True.
    """
    with imageio.get_writer(gif_name, mode="i",
                            duration=frame_duration) as writer:
        for file_name in file_names:
            image = imageio.imread(file_name)
            writer.append_data(image)
    if delete_files:
        for file in file_names:
            os.remove(file)


def combine_images(file_names: t.List[str],
                   image_name: str,
                   delete_files: bool=True) -> None:
    """Combines images horizontally.

    Args:
        file_names (t.List[str]): the list of names of the images.
        image_name: the name of the resulting image.
        delete_files (bool): whether the delete the original files,
            defaults to True.
    """
    images = [PIL.Image.open(i) for i in file_names]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_image = PIL.Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for image in images:
        new_image.paste(image, (x_offset,0))
        x_offset += image.size[0]
    new_image.save(image_name)
    if delete_files:
        for file in file_names:
            os.remove(file)


def add_text(file_name: str,
             position: t.Tuple[float],
             text: str,
             font_name: str,
             size: float,
             **kwargs) -> None:
    """Adds text to an image.

    Args:
        file_name (str): the list of name of the image.
        position (t.Tuple[float]): the position of the text.
        text (str): the text.
        font_name (str): the name of the font.
        size (float): the size of the text.
        kwargs: keyword arguments passed to PIL.ImageDraw.Draw.text().
    """
    image = PIL.Image.open(file_name)
    draw_image = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_name, size)
    draw_image.text(position, text, font = font, **kwargs)
    image.save(file_name)
      
