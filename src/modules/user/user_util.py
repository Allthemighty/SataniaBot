from sqlalchemy import func

from src import constants as const
from src.db_connection import Session
from src.modules.user.user_model import User

logger = const.logger


def user_exists(discord_id):
    """
    Checks if a user exists by id
    :param discord_id: Discord id
    :return: Boolean
    """
    session = Session()
    row = session.query(User).filter_by(uid=discord_id).first()
    session.close()
    return True if row else False


def get_user(discord_id):
    """
    Retrieve an user by id
    :param discord_id: Discord id
    :return: User
    """
    session = Session()
    user = session.query(User).filter_by(uid=discord_id).first()
    return user


def create_user(discord_id, discord_name, server_id, reaction_count=0):
    """
    Create an user and post it to the database
    :param discord_id: Discord id
    :param discord_name: Discord name (not nickname)
    :param server_id: From which server the user comes
    :param reaction_count: Amount of reactions that user triggered
    """
    session = Session()
    user = User(uid=discord_id,
                username=discord_name,
                from_server=server_id,
                reaction_count=reaction_count)
    session.add(user)
    session.commit()
    session.close()
    logger.info(f"Posted user to DB | {discord_id}: {discord_name} [{server_id}]")


def increment_reaction_counter(discord_id, inc_score):
    """
    Increment amount of reactions triggered by an user
    :param discord_id: Discord id
    :param inc_score: Amount to increment by
    """
    session = Session()
    user = get_user(discord_id)
    user.reaction_count += inc_score
    session.commit()
    session.close()


def get_users_paginated(low_bound, high_bound):
    """
    Get a list of users, between 2 values.
    :param low_bound: On which users to start matching
    :param high_bound: On which users to stop matching
    :return: list of users
    """
    session = Session()
    order = (User.reaction_count.desc(), User.username)
    row_number = func.row_number().over(order_by=order)
    query = session.query(User)
    query = query.add_column(row_number)
    query = query.from_self().filter(row_number.between(low_bound, high_bound))
    users = query.all()
    session.close()
    return users
