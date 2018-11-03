from db_connection import *
from models.reactions import Reaction
import re


# FIXME: Not properly detecting keywords yet
def get_reacts(msg):
    keywords = session.query(Reaction.keyword, Reaction.url).all()
    matches = []

    for keyword in keywords:
        match = re.search(r"\b" + msg + r"\b", keyword[0], re.IGNORECASE)
        if match:
            matches.append(keyword[1])
    if matches:
        return matches
