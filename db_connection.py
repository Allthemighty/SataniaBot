from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import constants as const

try:
    engine = create_engine(const.DATABASE_URL, connect_args={'sslmode': 'require'})
    Base = const.BASE
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
except:
    print("Cannot connect to db")
