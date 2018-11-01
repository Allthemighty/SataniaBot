from db_connection import *
from models.reactions import Reaction

def get_reacts(self):
    msg = self.lower()
    result = session.query(Reaction).filter(msg.like(Reaction.keyword))
    rows = result.all()
    if rows:
        return rows
