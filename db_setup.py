import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    artist = Column(String(70), nullable=False)
    genre = Column(String(35), nullable=False)
    release_date = Column(String(4), nullable=False)
    number_of_track = Column(String(2), nullable=False)
    cover = Column(String(300), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Returns object data in easily serializeable format
    @property
    def serialize(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "release_date": self.release_date,
            "number_of_track": self.number_of_track,
            "cover": self.cover
        }


engine = create_engine('sqlite:///music.db')


Base.metadata.create_all(engine)
