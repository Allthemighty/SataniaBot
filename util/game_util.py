from db_connection import *
from models.users import User


def user_exists(discord_id):
    """
    Checks if a user exists by id
    :param discord_id: Discord id
    :return: Boolean
    """
    row = session.query(User).filter_by(did=discord_id).first()
    return True if row else False


def user_get(discord_id):
    """
    Retrieve an user by id
    :param discord_id: Discord id
    :return: User
    """
    user = session.query(User).filter_by(did=discord_id).first()
    return user


def user_create(discord_id, discord_name, score=0, reactions_triggered=0):
    """
    Create an user
    :param discord_id: Discord id
    :param discord_name: Discord name (not nickname)
    :param score: Users score
    :param reactions_triggered: Amount of reactions that user triggered
    """
    user = User(did=discord_id, dname=discord_name, score=score,
                reactions_triggered=reactions_triggered)
    session.add(user)
    session.commit()
    print("Posted user to DB | {}: {}".format(discord_id, discord_name))


def increment_score(discord_id, inc_score):
    """
    Increment score of an user
    :param discord_id: Discord id
    :param inc_score: Amount to increment by
    """
    session.query(User).filter_by(did=discord_id).update({User.score: User.score + inc_score})
    session.commit()


def reduce_score(discord_id, red_score):
    """
    Reduce score of an user
    :param discord_id: Discord id
    :param red_score: Amount to decrease by
    """
    session.query(User).filter_by(did=discord_id).update({User.score: User.score - red_score})
    session.commit()


def multiply_score(discord_id, multiplier):
    """
    Multiply score of an user
    :param discord_id: Discord id
    :param multiplier: Amount to multiply by
    """
    session.query(User).filter_by(did=discord_id).update({User.score: User.score * multiplier})
    session.commit()


def increment_reaction_counter(discord_id, inc_score):
    """
    Increment amount of reactions triggered by an user
    :param discord_id: Discord id
    :param inc_score: Amount to increment by
    """
    session.query(User).filter_by(did=discord_id).update(
        {User.reactions_triggered: User.reactions_triggered + inc_score})
    session.commit()
