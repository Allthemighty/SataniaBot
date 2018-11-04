from sqlalchemy import Column, Integer, String

import constants as const


class Reaction(const.BASE):
    __tablename__ = 'reactions'

    iid = Column(Integer, primary_key=True)
    url = Column(String)
    keyword = Column(String)

    def __str__(self):
        return "ID: {}| URL {}| Keyword: {}".format(self.iid, self.url, self.keyword)
