from db_connection import *
from models.reactions import Reaction
import re


def get_reacts(msg):
    """
    Takes a message, and compares it against the database if it contains a matching keyword.
    All matches are reactions that will be returned
    :param msg: A string
    :return: A list of reactions,
    """
    keywords = session.query(Reaction.keyword, Reaction.url).all()
    matches = []

    for keyword in keywords:
        match = re.search(r"\b{}\b".format(keyword[0]), msg, re.IGNORECASE | re.M)
        if match:
            matches.append(keyword[1])
    if matches:
        return matches
