from datetime import datetime
from discord import Embed

from discord.colour import Colour

from typing import Optional, Union, Any, Dict



def create_embed(
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    colour: Optional[Union[int, Colour]] = None,
    color: Optional[Union[int, Colour]] = None,
    timestamp: Optional[datetime] = None,
    url: Optional[Any] = None,
) -> Embed:
    
    if colour is not None and color is not None:
        raise ValueError('Pass either \'colour\' or \'color\', not both.')
    
    colour = colour if colour is not None else color
    
    embed = Embed(
        title=title,
        description=description,
        colour=colour,
        timestamp=timestamp,
        url=url
    )

    return embed


def set_embed_attr(
    embed: Embed,
    image_url: Optional[Any] = None,
    author: Optional[Dict[str, str]] = None,
    footer: Optional[Dict[str, str]] = None,
    thumbnail: Optional[Any] = None
) -> Embed:

    """
    Sets optional attributes on a Discord embed.

    Args:
        embed (discord.Embed): The embed object to modify.
        image_url (Any | None): URL of the image to display in the embed.
        author (Dict[str, str] | None): 
            Keyword arguments to pass to `embed.set_author()`. 
            Supported keys:
                - "name" (str): The author's name.
                - "url" (str): A URL that the author's name will link to.
                - "icon_url" (str): A URL to the author's icon image.
        footer (Dict[str, str] | None): 
            Keyword arguments to pass to `embed.set_footer()`. 
            Supported keys:
                - "text" (str): The footer text.
                - "icon_url" (str): A URL to the footer's icon image.
        thumbnail (Any | None): URL of the thumbnail image for the embed.

    Returns:
        discord.Embed: The modified embed object.
    """

    func_arg_pairs = [
        (embed.set_image, image_url, {'url': image_url}),
        (embed.set_author, author, author),
        (embed.set_footer, footer, footer),
        (embed.set_thumbnail, thumbnail, {'url': thumbnail})
    ]
    
    for func, value, kwargs in func_arg_pairs:
        if value is not None:
            func(**kwargs)
    
    return embed