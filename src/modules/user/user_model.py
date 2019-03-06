from sqlalchemy import Column, BigInteger, Integer, String

from src import constants as const


class User(const.BASE):
    __tablename__ = 'user'

    uid = Column(BigInteger, primary_key=True)
    username = Column(String)
    reaction_count = Column(Integer)

    def __str__(self):
        return "ID: {}| Username {}| Reactions triggered: {}" \
            .format(self.uid, self.username, self.reaction_count)
