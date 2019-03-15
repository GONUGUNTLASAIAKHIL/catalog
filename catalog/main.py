from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, SeriesName, SerType, User
from flask import session as v_log_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

# to connect database

engine = create_engine('sqlite:///samsung.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "SAMSUNG SERIES"

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
pser_cat = session.query(SeriesName).all()


# User login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    v_log_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    pve_cat = session.query(SeriesName).all()
    sc = session.query(SerType).all()
    return render_template('login.html',
                           STATE=state, pser_cat=pser_cat, sc=sc)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != v_log_session['state']:
        vres = make_response(json.dumps('Invalid state parameter.'), 401)
        vres.headers['Content-Type'] = 'application/json'
        return vres
    # Obtain authorization code
    scode = request.data

    try:
        # Upgrade the authorization code into a credentials object
        voauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        voauth_flow.redirect_uri = 'postmessage'
        credentials = voauth_flow.step2_exchange(scode)
    except FlowExchangeError:
        vres = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        vres.headers['Content-Type'] = 'application/json'
        return vres

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    hp = httplib2.Http()
    result = json.loads(hp.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        vres = make_response(json.dumps(result.get('error')), 500)
        vres.headers['Content-Type'] = 'application/json'
        return vres

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        vres = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        vres.headers['Content-Type'] = 'application/json'
        return vres

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        vres = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        vres.headers['Content-Type'] = 'application/json'
        return vres

    stored_access_token = v_log_session.get('access_token')
    stored_gplus_id = v_log_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        vres = make_response(json.dumps(
            'Current user already connected.'), 200)
        vres.headers['Content-Type'] = 'application/json'
        return vres

    # Store the access token in the session for later use.
    v_log_session['access_token'] = credentials.access_token
    v_log_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    v_log_session['username'] = data['name']
    v_log_session['picture'] = data['picture']
    v_log_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(v_log_session['email'])
    if not user_id:
        user_id = createUser(v_log_session)
    v_log_session['user_id'] = user_id

    pop = ''
    pop += '<h1>Welcome, '
    pop += v_log_session['username']
    pop += '!</h1>'
    pop += '<img src="'
    pop += v_log_session['picture']
    pop += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % v_log_session['username'])
    print ("done!")
    return pop


# User Helper Functions
def createUser(v_log_session):
    FirstUser = User(name=v_log_session['username'], email=v_log_session[
                   'email'], picture=v_log_session['picture'])
    session.add(FirstUser)
    session.commit()
    user = session.query(User).filter_by(email=v_log_session['email']).one()
    return user.id


# Uet user information
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# get user email address
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# Home


@app.route('/')
@app.route('/home')
def home():
    pser_cat = session.query(SeriesName).all()
    return render_template('myhome.html', pser_cat=pser_cat)


# series  for admins


@app.route('/serie')
def serie():
    try:
        if v_log_session['username']:
            name = v_log_session['username']
            pser_cat = session.query(SeriesName).all()
            sm = session.query(SeriesName).all()
            sc = session.query(SerType).all()
            return render_template('myhome.html', pser_cat=pser_cat,
                                   sm=sm, sc=sc, uname=name)
    except:
        return redirect(url_for('showLogin'))

######
# Showing phones based on series 

@app.route('/serie/<int:scid>/AllCompanys')
def showPhones(scid):
    ''' displaying phones based on series'''
    pser_cat = session.query(SeriesName).all()
    sm = session.query(SeriesName).filter_by(id=scid).one()
    sc = session.query(SerType).filter_by(sernameid=scid).all()
    try:
        if v_log_session['username']:
            return render_template('showPhones.html', pser_cat=pser_cat,
                                   sm=sm, sc=sc,
                                   uname=v_log_session['username'])
    except:
        return render_template('showPhones.html',
                               pser_cat=pser_cat, sm=sm, sc=sc)


# Add New Mobile Series Company


@app.route('/serie/addSeries', methods=['POST', 'GET'])
def addSeries():
    ''' adding new mobile series'''
    if 'username' not in v_log_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if 'username' not in v_log_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        series = SeriesName(
            name=request.form['pname'],
            user_id=v_log_session['user_id'])
        session.add(series)
        session.commit()
        return redirect(url_for('serie'))
    else:
        return render_template(
            'addSeries.html', pser_cat=pser_cat)


# Edit Mobile Series Category


@app.route('/serie/<int:scid>/edit', methods=['POST', 'GET'])
def editSeries(scid):
    ''' Edit mobile series category'''
    if 'username' not in v_log_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editserie = session.query(SeriesName).filter_by(id=scid).one()
    creator = getUserInfo(editserie.user_id)
    user = getUserInfo(v_log_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != v_log_session['user_id']:
        flash("You cannot edit this  SAMSUNG SERIES."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('serie'))
    if request.method == "POST":
        if request.form['name']:
            editserie.name = request.form['name']
        session.add(editserie)
        session.commit()
        flash("Mobile Series Edited Successfully")
        return redirect(url_for('serie'))
    else:
        # pser_cat is global variable we can them in entire application
        return render_template('editSeries.html',
                               pt=editserie, pser_cat=pser_cat)


# Delete Mobile series Category

@app.route('/serie/<int:scid>/delete', methods=['POST', 'GET'])
def deleteSeries(scid):
    ''' Delete mobile categoty'''
    if 'username' not in v_log_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    pt = session.query(SeriesName).filter_by(id=scid).one()
    creator = getUserInfo(pt.user_id)
    user = getUserInfo(v_log_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != v_log_session['user_id']:
        flash("You cannot Delete this Mobile Series."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('serie'))
    if request.method == "POST":
        session.delete(pt)
        session.commit()
        flash("SERIES Company Deleted Successfully")
        return redirect(url_for('serie'))
    else:
        return render_template(
            'deleteSeries.html', pt=pt,
            pser_cat=pser_cat)


# Add New  Mobile Details


@app.route(
    '/serie/addSeries/addMobileDetails/<string:smname>/add',
    methods=['GET', 'POST'])
def addMobileDetails(smname):
    '''add new mobile details'''
    if 'username' not in v_log_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    sm = session.query(SeriesName).filter_by(name=smname).one()
    # See if the logged in user is not the owner of series
    creator = getUserInfo(sm.user_id)
    user = getUserInfo(v_log_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != v_log_session['user_id']:
        flash("You can't add new Mobile Details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('serie', scid=sm.id))
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        ram = request.form['ram']
        memory = request.form['memory']
        frontcamera = request.form['frontcamera']
        rearcamera = request.form['rearcamera']
        price = request.form['price']
        screen = request.form['screen']
        slink = request.form['slink']
        mobiledetails = SerType(name=name,
                                color=color,
                                ram=ram,
                                memory=memory,
                                frontcamera=frontcamera,
                                rearcamera=rearcamera,
                                price=price,
                                screen=screen,
                                slink=slink,
                                date=datetime.datetime.now(),
                                sernameid=sm.id,
                                user_id=v_log_session['user_id'])
        session.add(mobiledetails)
        session.commit()
        return redirect(url_for('serie', scid=sm.id))
    else:
        return render_template('addMobileDetails.html',
                               smname=sm.name, pser_cat=pser_cat)


# Edit Mobile  details


@app.route('/serie/<int:scid>/<string:smname>/edit',
           methods=['GET', 'POST'])
def editMobileDetails(scid, smname):
    ''' editing mobile details'''
    vb = session.query(SeriesName).filter_by(id=scid).one()
    mobiledetails = session.query(SerType).filter_by(
        name=smname).one()
    # See if the logged in user is not the owner of series
    creator = getUserInfo(vb.user_id)
    user = getUserInfo(v_log_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != v_log_session['user_id']:
        flash("You can't edit this Mobile Details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('serie', scid=vb.id))
    # POST methods
    if request.method == 'POST':
        mobiledetails.name = request.form['name']
        mobiledetails.color = request.form['color']
        mobiledetails. ram = request.form['ram']
        mobiledetails.memory = request.form['memory']
        mobiledetails.frontcamera = request.form['frontcamera']
        mobiledetails.rearcamera = request.form['rearcamera']
        mobiledetails. price = request.form['price']
        mobiledetails. screen = request.form['screen']
        mobiledetails.slink = request.form['slink']
        mobiledetails.date = datetime.datetime.now()
        session.add(mobiledetails)
        session.commit()
        flash("Mobile Details Edited Successfully")
        return redirect(url_for('serie', scid=scid))
    else:
        return render_template('editMobileDetails.html',
                               scid=scid, mobiledetails=mobiledetails,
                               pser_cat=pser_cat)


# Delte Mobile Details


@app.route('/serie/<int:scid>/<string:smname>/delete',
           methods=['GET', 'POST'])
def deleteMobileDetails(scid, smname):
    ''' delete mobiel details'''
    vb = session.query(SeriesName).filter_by(id=scid).one()
    mobiledetails = session.query(SerType).filter_by(
        name=smname).one()
    # See if the logged in user is not the owner of series
    creator = getUserInfo(vb.user_id)
    user = getUserInfo(v_log_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != v_log_session['user_id']:
        flash("You can't delete this Mobile details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('serie', scid=vb.id))
    if request.method == "POST":
        session.delete(mobiledetails)
        session.commit()
        flash("Deleted Mobile Details Successfully")
        return redirect(url_for('serie', scid=scid))
    else:
        return render_template('deleteMobileDetails.html',
                               scid=scid, mobiledetails=mobiledetails,
                               pser_cat=pser_cat)


# Logout from current user


@app.route('/logout')
def logout():
    ''' logout from current user'''
    access_token = v_log_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (v_log_session['username'])
    if access_token is None:
        print ('Access Token is None')
        vres = make_response(
            json.dumps('Current user not connected....'), 401)
        vres.headers['Content-Type'] = 'application/json'
        return response
    access_token = v_log_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    hp = httplib2.Http()
    result = \
        hp.request(uri=url, method='POST', body=None, headers={
            'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del v_log_session['access_token']
        del v_log_session['gplus_id']
        del v_log_session['username']
        del v_log_session['email']
        del v_log_session['picture']
        vres = make_response(json.dumps(
            'Successfully disconnected user..'), 200)
        vres.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        vres = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        vres.headers['Content-Type'] = 'application/json'
        return vres


# Json
####


@app.route('/serie/JSON')
def allserieJSON():
    mobilecategories = session.query(SeriesName).all()
    category_dict = [c.serialize for c in mobilecategories]
    for c in range(len(category_dict)):
        mobiles = [i.serialize for i in session.query(
                 SerType).filter_by(
                     sernameid=category_dict[c]["id"]).all()]
        if mobiles:
            category_dict[c]["mobile"] = mobiles
    return jsonify(SeriesName=category_dict)


@app.route('/serie/mobileserie/JSON')
def categoriesJSON():
    mobile = session.query(SeriesName).all()
    return jsonify(mobileCategories=[c.serialize for c in mobile])

####


@app.route('/serie/mobiles/JSON')
def itemsJSON():
    items = session.query(SerType).all()
    return jsonify(mobiles=[i.serialize for i in items])

#####


@app.route('/serie/<path:series_name>/serie/JSON')
def categoryItemsJSON(series_name):
    mobileCategory = session.query(
        SeriesName).filter_by(name=series_name).one()
    mobiles = session.query(SerType).filter_by(
        sername=mobileCategory).all()
    return jsonify(mobileEdtion=[i.serialize for i in mobiles])


@app.route('/serie/<path:series_name>/<path:mobile_name>/JSON')
def ItemJSON(series_name, mobile_name):
    mobileCategory = session.query(
        SeriesName).filter_by(name=series_name).one()
    mobileEdition = session.query(SerType).filter_by(
           name=mobile_name, sername=mobileCategory).one()
    return jsonify(mobileEdition=[mobileEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
