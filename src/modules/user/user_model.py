from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey

from src import constants as const


class User(const.BASE):
    __tablename__ = 'user'

    uid = Column(BigInteger, primary_key=True)
    username = Column(String)
    reaction_count = Column(Integer)
    from_server = Column(BigInteger, ForeignKey('server.server_id'), nullable=False)

    def __repr__(self):
        return (f"ID: [{self.uid}], "
                f"Username [{self.username}], "
                f"Reaction count: [{self.reaction_count}], "
                f"From_server: [{self.from_server}]")
