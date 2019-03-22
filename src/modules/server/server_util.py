from src.db_connection import Session
from src.modules.server.server_model import Server


def get_server(server_id):
    """
    Retrieve a server from the database
    :param server_id: Server id
    :return: Server object
    """
    session = Session()
    query = session.query(Server)
    query = query.filter_by(server_id=server_id)
    server = query.first()
    return server


def server_in_db(server_id):
    """
    Checks if a server is already in the database or not
    :param server_id: Server id
    :return: Boolean
    """
    return True if get_server(server_id) else False


def get_servers():
    """
    Retrieve all the discord servers in the database
    :return: List of servers
    """
    session = Session()
    servers = session.query(Server).all()
    return servers


def add_server(server_id, server_name):
    """
    Adds a server to the database
    :param server_id: Server id
    :param server_name: The server name
    """
    if not server_in_db(server_id):
        session = Session()
        new_server = Server(server_id=server_id, server_name=server_name)
        session.add(new_server)
        session.commit()
        session.close()


def remove_server(server_id):
    """
    Deletes a server from the database
    :param server_id: Server id
    """
    session = Session()
    session.query(Server).filter_by(server_id=server_id).delete()
    session.commit()
    session.close()


def refresh_servers(connected_servers):
    """
    Adds all connected servers to the database that are not in there, and removes all servers in
    the database that are not connected.
    :param connected_servers: Servers the bot is connected to
    """
    for server in connected_servers:
        add_server(server.id, server.name)


def set_message_chance(server_id, new_chance):
    """
    Set the message chance percentage of a server
    :param server_id: Server id
    :param new_chance: What percentage to set it to
    """
    session = Session()
    server = get_server(server_id)
    server.message_chance = new_chance
    session.commit()
    session.close()


def set_image_chance(server_id, new_chance):
    """
    Set the image chance percentage of a server
    :param server_id: Server id
    :param new_chance: What percentage to set it to
    """
    session = Session()
    server = get_server(server_id)
    server.image_chance = new_chance
    session.commit()
    session.close()
