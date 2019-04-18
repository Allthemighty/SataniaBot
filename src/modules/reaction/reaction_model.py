from ezstr import tostr
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from src import constants as const


@tostr
class Reaction(const.BASE):
    __tablename__ = 'reaction'

    reaction_id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(String)
    keyword = Column(String)
    react_type = Column(ENUM('gif', 'message'), name='react_type', nullable=False)
    from_server = Column(BigInteger, ForeignKey('server.server_id'), nullable=False)
