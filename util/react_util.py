from db_connection import *
from models.reactions import Reaction
import re


def get_reacts(msg, server_id, react_type='message'):
    """
    Takes a message, and compares it against the database if it contains a matching keyword.
    All matches are reactions that will be returned
    :param react_type: Whether the reaction to be send is a gif or a normal message
    :param msg: A string
    :return: A list of reactions,
    """
    query = session.query(Reaction.keyword, Reaction.url).filter_by(react_type=react_type,
                                                                    from_server=server_id)
    reactions = query.all()
    matches = []

    for reaction in reactions:
        keyword = reaction[0]
        url = reaction[1]
        match = re.search(r"\b{}\b".format(keyword), msg, re.IGNORECASE | re.M)
        if match:
            matches.append(url)
    if matches:
        return matches
