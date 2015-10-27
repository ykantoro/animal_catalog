from flask import Flask, render_template, request,\
    redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Animal, Species, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Set-up Flask Application
app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Animal Catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///speciesandanimals.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all species
@app.route('/', methods=['GET', 'POST'])
@app.route('/species/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def showSpecies():
    # Query all species alphabetically
    species = session.query(Species).order_by(asc(Species.name))
    # Listen for POST requests
    if request.method == 'POST':
        # Hidden form input in template will contain 'new'
        # if a new species is added.
        if request.form['new']:
            species = Species(
                name=request.form['name'],
                user_id=login_session['user_id'],
                picture=request.form['picture'])
            session.add(species)
            flash('New Species %s Successfully Created' % species.name)
            session.commit()
            return redirect(url_for('showSpecies'))
        # Hidden form input in template will contain 'edit'
        # if a new species is added. POST request from 'showAnimal'
        if request.form['edit']:
            species.name = request.form['nameedit']
            species.picture = request.form['pictureedit']
            flash('Species Successfully Edited %s' % species.name)
            return redirect(url_for('showSpecies'))
        # Hidden form input in template will contain 'delete'
        # if a new species is added. POST request from 'showAnimal'
        if request.form['delete']:
            species = session.query(Species).filter_by(id=int(
                request.form['delete'])).one()
            session.delete(species)
            flash('%s Successfully Deleted' % species.name)
            session.commit()
            return redirect(url_for('showSpecies'))
    else:
        return render_template('species.html', species=species,
                               loggedin=login_session)


# Show animals in specified species
@app.route('/species/<int:species_id>/', methods=['GET', 'POST'])
@app.route('/species/<int:species_id>/animals/', methods=['GET', 'POST'])
def showAnimal(species_id):
    species = session.query(Species).filter_by(id=species_id).one()
    animals = session.query(Animal).filter_by(species_id=species_id).all()
    user = session.query(User).filter_by(id=species.user_id).one()
    # Listen for POST request
    if request.method == 'POST':
        # Hidden form input in template will contain 'editanim'
        # if an animal is edited in a specie.
        if request.form['editanim']:
            animal = session.query(Animal).filter_by(id=int(
                request.form['editanim'])).one()
            if request.form['nameedit']:
                animal.name = request.form['nameedit']
            if request.form['descriptionedit']:
                animal.description = request.form['descriptionedit']
            if request.form['pictureedit']:
                animal.picture = request.form['pictureedit']
            if request.form['coloredit']:
                animal.color = request.form['coloredit']
            if request.form['sleepedit']:
                animal.sleep = request.form['sleepedit']
            if request.form['foodedit']:
                animal.food = request.form['foodedit']
            if request.form['weightedit']:
                animal.weight = request.form['weightedit']
            session.add(animal)
            session.commit()
            flash('Animal %s Successfully Edited' % animal.name)
            return redirect(url_for('showAnimal', species_id=species_id))
        # Hidden form input in template will contain 'deleteanim'
        # if an animal is deleted from a species.
        if request.form['deleteanim']:
            animal = session.query(Animal).filter_by(id=int(
                request.form['deleteanim'])).one()
            store = animal.name
            session.delete(animal)
            session.commit()
            flash('Animal %s Successfully Deleted' % store)
            return redirect(url_for('showAnimal', species_id=species_id))
        # Hidden form input in template will contain 'newanim'
        # if a new animal is added to a species.
        if request.form['newanim']:
            newAnimal = Animal(name=request.form['name'],
                               description=request.form['description'],
                               picture=request.form['picture'],
                               sleep=request.form['sleep'],
                               color=request.form['color'],
                               weight=request.form['weight'],
                               food=request.form['food'],
                               species_id=species_id,
                               user_id=species.user_id)
            session.add(newAnimal)
            session.commit()
            flash('New Animal %s Successfully Created' % (newAnimal.name))
            return redirect(url_for('showAnimal', species_id=species_id))
    else:
        return render_template('animals.html', animals=animals,
                               species=species, user=user,
                               loggedin=login_session)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Login to site via Facebook
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = '''https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s''' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.2/me?%s' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s" % url
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in
    # our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = '''https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']

    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += '''" style = "width: 100px; height: 100px;border-radius: 75px;\
                -webkit-border-radius: 75px;-moz-border-radius: 75px;"> '''

    flash("Now logged in as %s" % login_session['username'])
    return output


# Login to site via Google Plus
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

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
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user is already\
        connected.'''), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 100px; height: 100px;border-radius: 75px;\
                -webkit-border-radius: 75px;-moz-border-radius: 75px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
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


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    # Only disconnect a connected user, if they are not
    # already logged in.
    if login_session['username']:
        if login_session['provider'] == 'google':
            url = '''https://accounts.google.com/o/oauth2/revoke?token=%s''' % access_token
            h = httplib2.Http()
            result = h.request(url, 'GET')[0]
            if result['status'] == '200':
                # Reset the user's sesson.
                del login_session['access_token']
                del login_session['gplus_id']
                del login_session['username']
                del login_session['email']
                del login_session['picture']
                del login_session['provider']
                del login_session['user_id']

                response = make_response(json.dumps('''Successfully disconnected.'''), 200)
                response.headers['Content-Type'] = 'application/json'
                return redirect(url_for('showSpecies'))
        if login_session['provider'] == 'facebook':
            print "at fb logout"
            facebook_id = login_session['facebook_id']
            # The access token must me included to successfully logout
            access_token = login_session['access_token']
            url = '''https://graph.facebook.com/%s%s/permissions''' % (facebook_id, access_token)
            h = httplib2.Http()
            result = h.request(url, 'DELETE')[1]
            # Reset the user's sesson.
            del login_session['access_token']
            del login_session['facebook_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['provider']
            del login_session['user_id']
            return redirect(url_for('showSpecies'))
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Restaurant Information
@app.route('/species/<int:species_id>/animals/JSON')
def specieAnimals(species_id):
    species = session.query(Species).filter_by(id=species_id).one()
    animal = session.query(Animal).filter_by(
        species_id=species_id).all()
    return jsonify(Animal=[i.serialize for i in animal])


@app.route('/species/<int:species_id>/animals/<int:animal_id>/JSON')
def animalSON(species_id, animal_id):
    animal = session.query(Animal).filter_by(id=animal_id).one()
    return jsonify(animal=animal.serialize)


@app.route('/species/JSON')
def speciesJSON():
    species = session.query(Species).all()
    return jsonify(species=[r.serialize for r in species])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
