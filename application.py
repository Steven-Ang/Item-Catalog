# Import all of the necessary modules for the project
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Album

app = Flask(__name__)

# Connect to the database
engine = create_engine('sqlite:///music.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all of the existing albums
# from the database on the page "/albums/"
# and the root of the web application.
@app.route("/albums/")
@app.route("/")
def showAlbums():
    albums = session.query(Album).all()
    return render_template("catalog.html", albums=albums)


# Show individual album
@app.route("/albums/<int:album_id>/")
def showAlbum(album_id):
    album = session.query(Album).filter_by(id=album_id).one()
    return render_template("album.html", album=album)


# Authenticated users have the ability to add new album to the database
# by going to the page "/albums/new".
# Unauthenticated users are not permitted to access this page.
@app.route("/albums/new/", methods=["GET", "POST"])
def createAlbum():
    if request.method == "POST":
        newAlbum = Album(
            title=request.form['title'],
            artist=request.form["artist"],
            genre=request.form["genre"],
            release_date=request.form["release_date"],
            number_of_track=request.form["number_of_track"],
            cover=request.form["cover"])
        session.add(newAlbum)
        session.commit()
        flash("Success! A new album has been added to the database!")
        return redirect(url_for('showAlbums'))
    else:
        return render_template("createAlbum.html")


# Edit album from the database
@app.route("/albums/edit/<int:album_id>/", methods=["GET", "POST"])
def editAlbum(album_id):
    albumToEdit = session.query(Album).filter_by(id=album_id).one()
    if request.method == "POST":
        if request.form["title"]:
            albumToEdit.title = request.form["title"]
            albumToEdit.artist = request.form["artist"]
            albumToEdit.genre = request.form["genre"]
            albumToEdit.release_date = request.form["release_date"]
            albumToEdit.number_of_track = request.form["number_of_track"]
            albumToEdit.cover = request.form["cover"]
            session.add(albumToEdit)
            session.commit()
            flash("Success! The album has been edited!")
        return redirect(url_for("showAlbums"))
    else:
        return render_template("editAlbum.html", album=albumToEdit, album_id=album_id)


# Delete album from the database
@app.route("/albums/delete/<int:album_id>/", methods=["GET", "POST"])
def deleteAlbum(album_id):
    albumToDelete = session.query(Album).filter_by(id=album_id).one()
    if request.method == "POST":
        session.delete(albumToDelete)
        session.commit()
        flash("Success! One album has been removed from the database!")
        return redirect(url_for("showAlbums"))
    else:
        return render_template("deleteAlbum.html", album=albumToDelete, album_id=album_id)



if __name__ == "__main__":
    app.secret_key = "DoctorWantsToEatSomeTaco!"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
