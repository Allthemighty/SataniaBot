from ezstr import tostr
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey

from src import constants as const


@tostr
class User(const.BASE):
    __tablename__ = 'user'

    uid = Column(BigInteger, primary_key=True)
    username = Column(String)
    reaction_count = Column(Integer)
    from_server = Column(BigInteger, ForeignKey('server.server_id'), nullable=False)
