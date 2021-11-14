from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data.config import DATABASE_NAME


engine = create_engine(f'sqlite:///{DATABASE_NAME}', connect_args={'check_same_thread': False})
session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
