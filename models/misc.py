from sqlalchemy import Column, String, Integer

import constants as const


class Misc(const.BASE):
    __tablename__ = 'misc'

    index = Column(Integer, primary_key=True)
    status_playing = Column(String)
