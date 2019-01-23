from db_connection import *
from modules.user.user_model import User
from sqlalchemy import func

logger = const.logger


def user_exists(discord_id):
    """
    Checks if a user exists by id
    :param discord_id: Discord id
    :return: Boolean
    """
    row = session.query(User).filter_by(did=discord_id).first()
    return True if row else False


def get_user(discord_id):
    """
    Retrieve an user by id
    :param discord_id: Discord id
    :return: User
    """
    query = session.query(User)
    query = query.filter_by(did=discord_id)
    return query.first()


def create_user(discord_id, discord_name, reactions_triggered=0):
    """
    Create an user
    :param discord_id: Discord id
    :param discord_name: Discord name (not nickname)
    :param reactions_triggered: Amount of reactions that user triggered
    """
    user = User(did=discord_id, dname=discord_name, reactions_triggered=reactions_triggered)
    session.add(user)
    session.commit()
    logger.info(f"Posted user to DB | {discord_id}: {discord_name}")


def increment_reaction_counter(discord_id, inc_score):
    """
    Increment amount of reactions triggered by an user
    :param discord_id: Discord id
    :param inc_score: Amount to increment by
    """
    user = get_user(discord_id)
    user.reactions_triggered += inc_score
    session.commit()


def get_users_paginated(low_bound, high_bound):
    """
    Get a list of users, between 2 values.
    :param low_bound: On which users to start matching
    :param high_bound: On which users to stop matching
    :return: list of users
    """
    order = (User.reactions_triggered.desc(), User.dname)
    row_number = func.row_number().over(order_by=order)
    query = session.query(User)
    query = query.add_column(row_number)
    query = query.from_self().filter(row_number.between(low_bound, high_bound))
    return query.all()
