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
    session.close()
    return server


def get_servers():
    """
    Retrieve all the discord servers in the database
    :return: List of servers
    """
    session = Session()
    servers = session.query(Server).all()
    session.close()
    return servers


def add_server(server_id, server_name):
    """
    Adds a server to the database
    :param server_id: Server id
    :param server_name: The server name
    """
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


def refresh_servers(connected_servers, database_servers=get_servers()):
    """
    Adds all connected servers to the database that are not in there, and removes all servers in
    the database that are not connected.
    :param connected_servers: Servers the bot is connected to
    :param database_servers: Servers in the database
    """
    for server in connected_servers:
        if server.id not in [server.server_id for server in database_servers]:
            add_server(server.id, server.name)
    for server in database_servers:
        if server.server_id not in [server.id for server in connected_servers]:
            pass


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


def set_gif_chance(server_id, new_chance):
    """
    Set the gif chance percentage of a server
    :param server_id: Server id
    :param new_chance: What percentage to set it to
    """
    session = Session()
    server = get_server(server_id)
    server.gif_chance = new_chance
    session.commit()
    session.close()
