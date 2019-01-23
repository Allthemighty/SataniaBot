from db_connection import *
from modules.server.server_model import Server


def get_server(server_id):
    """
    Retrieve a server from the database
    :param server_id: Server id
    :return: Server object
    """
    query = session.query(Server)
    query = query.filter_by(server_id=server_id)
    return query.first()


def set_message_chance(server_id, new_chance):
    """
    Set the message chance percentage of a server
    :param server_id: Server id
    :param new_chance: What percentage to set it to
    """
    server = get_server(server_id)
    server.message_chance = new_chance
    session.commit()


def set_gif_chance(server_id, new_chance):
    """
    Set the gif chance percentage of a server
    :param server_id: Server id
    :param new_chance: What percentage to set it to
    """
    server = get_server(server_id)
    server.gif_chance = new_chance
    session.commit()
