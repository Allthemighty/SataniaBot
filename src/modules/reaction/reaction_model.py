from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from src import constants as const


class Reaction(const.BASE):
    __tablename__ = 'reaction'

    reaction_id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(String)
    keyword = Column(String)
    react_type = Column(ENUM('gif', 'message'), name='react_type', nullable=False)
    from_server = Column(BigInteger, ForeignKey('server.server_id'), nullable=False)

    def __repr__(self):
        return (f"ID: [{self.reaction_id}], "
                f"URL [{self.answer}], "
                f"Keyword: [{self.keyword}], "
                f"Type: [{self.react_type}], "
                f"From_server: [{self.from_server}]")
