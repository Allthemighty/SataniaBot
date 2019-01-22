from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

import constants as const


class Reaction(const.BASE):
    __tablename__ = 'reaction'

    reaction_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    keyword = Column(String)
    react_type = Column(ENUM('gif', 'message'), name='react_type', nullable=False)
    from_server = Column(BigInteger, ForeignKey('server.server_id'), nullable=False)

    def __str__(self):
        return (f"ID: {self.reaction_id}| URL {self.url}| "
                f"Keyword: {self.keyword}, Type: {self.react_type}")
