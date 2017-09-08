import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    artist = Column(String(70), nullable=False)
    genre = Column(String(35), nullable=False)
    release_date = Column(String(4), nullable=False)
    number_of_track = Column(String(2), nullable=False)
    cover = Column(String(300), nullable=False)


engine = create_engine('sqlite:///music.db')


Base.metadata.create_all(engine)
