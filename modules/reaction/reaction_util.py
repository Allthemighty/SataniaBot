import re

from sqlalchemy import func

from db_connection import *
from modules.reaction.reaction_model import Reaction


def get_reactions(message, server_id, react_type='message'):
    """
    Takes a message, and compares it against the database if it contains a matching keyword.
    All matches are reactions that will be returned.
    :param server_id: From which server the reactions are
    :param react_type: Whether the reaction to be sent is a gif or a normal message
    :param message: A string
    :return: A list of reactions,
    """
    query = session.query(Reaction.keyword, Reaction.url).filter_by(react_type=react_type,
                                                                    from_server=server_id)
    reactions = query.all()
    matches = []

    for reaction in reactions:
        keyword = reaction[0]
        url = reaction[1]
        match = re.search(r"\b{}\b".format(keyword), message, re.IGNORECASE | re.M)
        if match:
            matches.append(url)
    if matches:
        return matches


def add_reaction(url, keyword, react_type, server_id):
    """
    Add a reaction to the database
    :param url: What to send back when sending a message as response
    :param keyword: On what keyword to match
    :param react_type: Whether the reaction to be sent is a gif or a normal message
    :param server_id: From which server the reaction belongs to
    """
    try:
        reaction = Reaction(url=url, keyword=keyword, react_type=react_type, from_server=server_id)
        session.add(reaction)
        session.commit()
    except:
        logger.error('Error when commiting reaction to database')


def delete_reaction(reaction_id):
    """
    Delete a reaction from the database
    :param reaction_id: The id of the reaction
    """
    session.query(Reaction).filter_by(reaction_id=reaction_id).delete()
    session.commit()


def get_reactions_paginated(low_bound, high_bound, server_id):
    """
    Get a list of reactions, between 2 values.
    :param low_bound: On which reactions to start matching
    :param high_bound: On which reactions to stop matching
    :param server_id: From which server the reaction belongs to
    :return: list of reactions
    """
    row_number = func.row_number().over(order_by=Reaction.reaction_id)
    query = session.query(Reaction.reaction_id,
                          Reaction.url,
                          Reaction.keyword,
                          Reaction.from_server)
    query = query.filter_by(from_server=server_id)
    query = query.add_column(row_number)
    query = query.from_self().filter(row_number.between(low_bound, high_bound))
    return query.all()
