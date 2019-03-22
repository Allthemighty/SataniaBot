import re

from sqlalchemy import func

from src.constants import *
from src.db_connection import Session
from src.modules.reaction.reaction_model import Reaction


def get_matching_reactions(message, server_id, react_type='message'):
    """
    Takes a message, and compares it against the database if it contains a matching keyword.
    All matches are reactions that will be returned.
    :param server_id: From which server the reactions are
    :param react_type: Whether the reaction to be sent is a gif or a normal message
    :param message: A string
    :return: A list of reactions,
    """
    session = Session()
    query = session.query(Reaction.keyword, Reaction.answer)
    query = query.filter_by(react_type=react_type, from_server=server_id)
    reactions = query.all()
    session.close()
    matches = []

    for reaction in reactions:
        keyword = reaction[0]
        answer = reaction[1]
        match = re.search(r"\b{}\b".format(keyword), message, re.IGNORECASE | re.M)
        if match:
            matches.append(answer)
    if matches:
        return matches


def get_reaction(reaction_id, server_id):
    """
    Gets a reaction by its id
    :param reaction_id: Reaction id
    :param server_id: Server id
    :return: Reaction object
    """
    session = Session()
    query = session.query(Reaction)
    query = query.filter_by(reaction_id=reaction_id, from_server=server_id)
    reaction = query.first()
    return reaction


def add_reaction(answer, keyword, react_type, server_id):
    """
    Add a reaction to the database
    :param answer: What to send back as response
    :param keyword: On what keyword to match
    :param react_type: Whether the reaction to be sent is a gif or a normal message
    :param server_id: From which server the reaction belongs to
    """
    try:
        session = Session()
        reaction = Reaction(answer=answer, keyword=keyword, react_type=react_type,
                            from_server=server_id)
        session.add(reaction)
        session.commit()
        session.close()
    except:
        logger.error('Error when commiting reaction to database', exc_info=True)


def delete_reaction(reaction_id):
    """
    Delete a reaction from the database
    :param reaction_id: The id of the reaction
    """
    session = Session()
    session.query(Reaction).filter_by(reaction_id=reaction_id).delete()
    session.commit()
    session.close()


def update_keyword(reaction_id, server_id, keyword):
    """
    Update the keyword of a reaction
    :param reaction_id: Reaction id
    :param server_id: Server id
    :param keyword: Keyword to update
    """
    session = Session()
    reaction = session.query(Reaction).filter_by(reaction_id=reaction_id,
                                                 from_server=server_id).first()
    reaction.keyword = keyword
    session.commit()
    session.close()


def update_answer(reaction_id, server_id, answer):
    """
    Update the keyword of a reaction
    :param reaction_id: Reaction id
    :param server_id: Server id
    :param answer: Answer to update
    """
    session = Session()
    reaction = session.query(Reaction).filter_by(reaction_id=reaction_id,
                                                 from_server=server_id).first()
    reaction.answer = answer
    session.commit()
    session.close()


def get_reactions_paginated(low_bound, high_bound, server_id):
    """
    Get a list of reactions, between 2 values.
    :param low_bound: On which reactions to start matching
    :param high_bound: On which reactions to stop matching
    :param server_id: From which server the reaction belongs to
    :return: list of reactions
    """
    session = Session()
    row_number = func.row_number().over(order_by=Reaction.reaction_id)
    query = session.query(Reaction.reaction_id,
                          Reaction.answer,
                          Reaction.keyword,
                          Reaction.from_server)
    query = query.filter_by(from_server=server_id)
    query = query.add_column(row_number)
    query = query.from_self().filter(row_number.between(low_bound, high_bound))
    reactions = query.all()
    session.close()
    return reactions
