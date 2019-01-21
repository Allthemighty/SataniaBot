import re

import requests
from discord.embeds import Colour
from sqlalchemy import text

from db_connection import *
from models.misc import Misc
from models.server import Server


def get_advice():
    """
    Calls the adviceslip API, and gets a piece of advice
    :return: Advice in string
    """
    response = requests.get(url='http://api.adviceslip.com/advice')
    advice = response.json()['slip']['advice']
    return advice


def connected_to_db():
    """
    Queries the database to check if the connection is live
    :return: Boolean
    """
    try:
        session.execute(text('SELECT 1'))
        return True
    except:
        return False


def change_status(activity):
    """
    Changes the playing status in the database
    :param activity:
    """
    session.query(Misc).first().status_playing = activity
    session.commit()


def get_status():
    """
    Gets the playing status from the database
    :return: playing status
    """
    return session.query(Misc).first().status_playing


def get_discord_colors():
    """
    This is used to get a list of colors that can be used in Embeds
    :return: A collection of discord colors in a dictionary
    """
    discord_colors = {'red': Colour.red(), 'dark_red': Colour.dark_red(),
                      'green': Colour.green(), 'dark_green': Colour.dark_green(),
                      'blue': Colour.blue(), 'dark_blue': Colour.dark_blue(),
                      'teal': Colour.teal(), 'dark_teal': Colour.dark_teal(),
                      'purple': Colour.purple(), 'dark_purple': Colour.dark_purple(),
                      'magenta': Colour.magenta(), 'dark_magenta': Colour.dark_magenta(),
                      'gold': Colour.gold(), 'dark_gold': Colour.dark_gold(),
                      'orange': Colour.orange(), 'dark_orange': Colour.dark_orange(),
                      'light_grey': Colour.light_grey(), 'lighter_grey': Colour.lighter_grey(),
                      'dark_grey': Colour.dark_grey(), 'darker_grey': Colour.darker_grey(),
                      'blurple': Colour.blurple(), 'greyple': Colour.greyple()}
    return discord_colors


def is_hex_color(hex_color):
    """
    Asserts if a string is a hex color or not
    :param hex_color: string to match
    :return: boolean
    """
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color)
    return match


def hex_to_rgb(hex_color):
    """Converts a hex color code to RGB, to a Discord Color"""
    hex_code = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))
    return Colour.from_rgb(rgb_color[0], rgb_color[1], rgb_color[2])


def get_servers():
    """
    Retrieve all the discord servers in the database
    :return: List of servers
    """
    return session.query(Server).all()


def add_server(server_id, server_name):
    """
    Adds a server to the database
    :param server_id: The server id
    :param server_name: The server name
    """
    new_server = Server(server_id=server_id, server_name=server_name)
    session.add(new_server)
    session.commit()
