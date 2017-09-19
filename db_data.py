from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Album, Base

engine = create_engine('sqlite:///music.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# List of Albums
album_1 = Album(title="Room for Squares",
                artist="John Mayer",
                genre="Rock",
                release_date="2001",
                number_of_track="13",
                cover="https://images-na.ssl-images-amazon.com/images/I/81xGr0YG-IL._SY355_.jpg")   # noqa

session.add(album_1)
session.commit()

album_2 = Album(title="Heavier Things",
                artist="John Mayer",
                genre="Rock",
                release_date="2003",
                number_of_track="10",
                cover="https://images-na.ssl-images-amazon.com/images/I/81s%2Bgnc7XsL._SX425_.jpg")   # noqa

session.add(album_2)
session.commit()

album_3 = Album(title="Continuum",
                artist="John Mayer",
                genre="Rock",
                release_date="2006",
                number_of_track="12",
                cover="https://vignette3.wikia.nocookie.net/lyricwiki/images/d/de/John_Mayer_-_Continuum_%28alt%29.jpg/revision/latest?cb=20121018083846")   # noqa

session.add(album_3)
session.commit()

album_4 = Album(title="Battle Studies",
                artist="John Mayer",
                genre="Rock",
                release_date="2009",
                number_of_track="11",
                cover="https://upload.wikimedia.org/wikipedia/en/a/a7/JohnMayerBattleStudies.jpg")   # noqa

session.add(album_4)
session.commit()

album_5 = Album(title="Born and Raised",
                artist="John Mayer",
                genre="Rock",
                release_date="2012",
                number_of_track="12",
                cover="http://davidadriansmith.com/wp-content/uploads//2012/05/mayer_font.jpg")   # noqa

session.add(album_5)
session.commit()

album_6 = Album(title="Paradise Valley",
                artist="John Mayer",
                genre="Rock",
                release_date="2013",
                number_of_track="11",
                cover="https://upload.wikimedia.org/wikipedia/en/5/5c/Paradise_Valley_cover%2C_by_John_Mayer.jpg")   # noqa

session.add(album_6)
session.commit()


print("Successfully added the data into the database.")
