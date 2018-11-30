from db_connection import *
from models.users import Users


def user_exists(discord_id):
    """
    Checks if a user exists by id
    :param discord_id: Discord id
    :return: Boolean
    """
    row = session.query(Users).filter_by(did=discord_id).first()
    return True if row else False


def user_get(discord_id):
    """
    Retrieve an user by id
    :param discord_id: Discord id
    :return: User
    """
    user = session.query(Users).filter_by(did=discord_id).first()
    return user


def user_create(discord_id, discord_name, reactions_triggered=0):
    """
    Create an user
    :param discord_id: Discord id
    :param discord_name: Discord name (not nickname)
    :param score: Users score
    :param reactions_triggered: Amount of reactions that user triggered
    """
    user = Users(did=discord_id, dname=discord_name,
                 reactions_triggered=reactions_triggered)
    session.add(user)
    session.commit()
    print("Posted user to DB | {}: {}".format(discord_id, discord_name))


def increment_reaction_counter(discord_id, inc_score):
    """
    Increment amount of reactions triggered by an user
    :param discord_id: Discord id
    :param inc_score: Amount to increment by
    """
    session.query(Users).filter_by(did=discord_id).update(
        {Users.reactions_triggered: Users.reactions_triggered + inc_score})
    session.commit()
