import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import src.constants as const
from src.secrets import DATABASE_URL

logger = const.logger


def init_sessionmaker():
    try:
        engine = create_engine(DATABASE_URL,
                               connect_args={'sslmode': 'require'},
                               pool_size=50)
        base = const.BASE
        base.metadata.create_all(engine)
        return sessionmaker(bind=engine)
    except:
        logger.critical(f'Cannot connect to database: {traceback.format_exc()}')


session_factory = init_sessionmaker()
Session = scoped_session(session_factory)
