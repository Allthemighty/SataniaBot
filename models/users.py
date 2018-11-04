from sqlalchemy import Column, BigInteger, Integer, String

import constants as const


class User(const.BASE):
    __tablename__ = 'users'

    did = Column(BigInteger, primary_key=True)
    dname = Column(String)
    score = Column(BigInteger)
    reactions_triggered = Column(Integer)

    def __str__(self):
        return "ID: {}| Username {}| Score: {}| Reactions triggered: {}" \
            .format(self.did, self.dname, self.score, self.reactions_triggered)
