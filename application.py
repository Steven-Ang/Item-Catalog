# Import all of the necessary modules for the project
from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Album, User

# Import modules for authentication
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from functools import wraps
import random
import string
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Album Catalog"


# Connect to the database
engine = create_engine('sqlite:///music.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# To check whether the user is authenticated to view the page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in login_session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Show all of the existing albums
# from the database on the page "/albums/"
# and the root of the web application.
@app.route("/albums/")
@app.route("/")
def showAlbums():
    albums = session.query(Album).all()
    if 'username' not in login_session:
        return render_template('publicAlbums.html', albums=albums)
    else:
        return render_template('catalog.html', albums=albums)


# Show individual album
@app.route("/albums/<int:album_id>/")
def showAlbum(album_id):
    album = session.query(Album).filter_by(id=album_id).one()
    return render_template("album.html", album=album)


# Authenticated users have the ability to add new album to the database
# by going to the page "/albums/new".
# Unauthenticated users are not permitted to access this page.
@app.route("/albums/new/", methods=["GET", "POST"])
@login_required
def createAlbum():
    if request.method == "POST":
        newAlbum = Album(
            title=request.form['title'],
            artist=request.form["artist"],
            genre=request.form["genre"],
            release_date=request.form["release_date"],
            number_of_track=request.form["number_of_track"],
            cover=request.form["cover"],
            user_id=login_session['user_id'])
        session.add(newAlbum)
        session.commit()
        flash("Success! A new album has been added to the database!")
        return redirect(url_for('showAlbums'))
    else:
        return render_template("createAlbum.html")


# Edit album from the database
@app.route("/albums/edit/<int:album_id>/", methods=["GET", "POST"])
@login_required
def editAlbum(album_id):
    albumToEdit = session.query(Album).filter_by(id=album_id).one()
    if albumToEdit.user_id != login_session['user_id']:
        return """<script>(function(evenet) {alert(
    "You don't have the permission to edit this item." +
    "It does not belong to you.");})();</script>"""
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
        return render_template(
            "editAlbum.html",
            album=albumToEdit,
            album_id=album_id)


# Delete album from the database
@app.route("/albums/delete/<int:album_id>/", methods=["GET", "POST"])
@login_required
def deleteAlbum(album_id):
    albumToDelete = session.query(Album).filter_by(id=album_id).one()
    if albumToDelete.user_id != login_session['user_id']:
        return """<script>(function() {alert(
    "You don't have the permission to delete this item." +
    "It does not belong to you.");})();</script>"""
    if request.method == "POST":
        session.delete(albumToDelete)
        session.commit()
        flash("Success! One album has been removed from the database!")
        return redirect(url_for("showAlbums"))
    else:
        return render_template(
            "deleteAlbum.html",
            album=albumToDelete,
            album_id=album_id)


# Endpoint for the all of the album from the catalog
@app.route("/albums/JSON/")
def showAlbumsJson():
    albumsJSON = session.query(Album).all()
    return jsonify(Album=[i.serialize for i in albumsJSON])


# Endpoint for individual album
@app.route("/albums/<int:album_id>/JSON/")
def showAlbumJson(album_id):
    albumJSON = session.query(Album).filter_by(id=album_id).one()
    return jsonify(Album=albumJSON.serialize)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome'
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You're now logged in.")
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showAlbums'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showAlbums'))


if __name__ == "__main__":
    app.secret_key = "DoctorWantsToEatSomeTaco!"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
