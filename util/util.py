import validators
import requests
from db_connection import *
from sqlalchemy import text


def url_remove(reaction_list, keep_url=True):
    """
    Iterates over a list, and either removes or keeps the items inside it, depending on if they
    contain an url
    :param reaction_list: List to iterate over
    :param keep_url: If true, it will keep all the items with an url in it, the reverse for false
    :return: The filtered list
    """
    if keep_url:
        for idx, item in enumerate(reaction_list):
            if not validators.url(item):
                reaction_list.pop(idx)
    else:
        for idx, item in enumerate(reaction_list):
            if validators.url(item):
                reaction_list.pop(idx)
    return reaction_list


def get_advice():
    """
    Calls the adviceslip API, and gets a piece of advice
    :return: Advice in string
    """
    response = requests.get(url='http://api.adviceslip.com/advice')
    advice = response.json()['slip']['advice']
    return advice


def connected_to_db():
    try:
        session.execute(text('SELECT 1'))
        return True
    except:
        return False
