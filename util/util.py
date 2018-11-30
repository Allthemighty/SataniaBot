import requests
from discord.embeds import Colour
from sqlalchemy import text

from db_connection import *
from models.misc import Misc


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
