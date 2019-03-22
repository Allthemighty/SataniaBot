from sqlalchemy import Column, Integer, BigInteger, String

from src import constants as const


class Server(const.BASE):
    __tablename__ = 'server'

    server_id = Column(BigInteger, primary_key=True)
    server_name = Column(String, nullable=False)
    message_chance = Column(Integer, default=25)
    image_chance = Column(Integer, default=10)

    def __str__(self):
        return f"server_id: {self.server_id}, server_name: {self.server_name}"
