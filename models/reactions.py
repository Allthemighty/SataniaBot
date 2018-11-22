from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM

import constants as const


class Reaction(const.BASE):
    __tablename__ = 'reactions'

    iid = Column(Integer, primary_key=True)
    url = Column(String)
    keyword = Column(String)
    react_type = Column(ENUM('gif', 'message'), name='react_type', nullable=False)

    def __str__(self):
        return f"ID: {self.iid}| URL {self.url}| " \
               f"Keyword: {self.keyword}, Reaction Type: {self.react_type}"
