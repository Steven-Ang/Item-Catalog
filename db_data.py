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
                genre="Rock", release_date="2001",
                number_of_track="13",
                cover="https://images-na.ssl-images-amazon.com/images/I/81xGr0YG-IL._SY355_.jpg")

session.add(album_1)
session.commit()

album_2 = Album(title="Between Two lungs",
                artist="Florence and The Machine",
                genre="Alternative", release_date="2010",
                number_of_track="12",
                cover="https://upload.wikimedia.org/wikipedia/en/2/26/Florence_and_the_Machine_-_Lungs.png")

session.add(album_2)
session.commit()

album_3 = Album(title="Frank",
                artist="Amy Winehouse",
                genre="Soul",
                release_date="2001",
                number_of_track="13",
                cover="https://upload.wikimedia.org/wikipedia/en/e/e5/Amy_Winehouse_-_Frank.png")

session.add(album_3)
session.commit()

album_4 = Album(title="One In a Million",
                artist="Aaliyah",
                genre="R&B", release_date="1996",
                number_of_track="17",
                cover="https://vignette3.wikia.nocookie.net/lyricwiki/images/f/f6/Aaliyah_-_One_in_a_Million.jpg/revision/latest?cb=20080423131927")

session.add(album_4)
session.commit()

album_5 = Album(title="Melodrama",
                artist="Lorde",
                genre="Pop",
                release_date="2017",
                number_of_track="11",
                cover="https://assets.vogue.com/photos/58b9984661298051ac278def/master/pass/00-holding-lorde-album-art.jpg")

session.add(album_5)
session.commit()


print("Successfully added the data into the database.")
