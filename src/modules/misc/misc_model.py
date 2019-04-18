from ezstr import tostr
from sqlalchemy import Column, String, Integer

from src import constants as const


@tostr
class Misc(const.BASE):
    __tablename__ = 'misc'

    index = Column(Integer, primary_key=True)
    status_playing = Column(String)
