import requests
import validators
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
