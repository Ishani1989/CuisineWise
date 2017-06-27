#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Cuisine, Dish, User
from flask import session as login_session
from datetime import datetime
import random
import string
import logging

# IMPORTS FOR THIS STEP

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

httplib2.debuglevel = 4

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']
['client_id']
APPLICATION_NAME = 'Restaurant Menu Application'

UPLOAD_FOLDER = 'D:\softwares\Eclipse\workspace\CuisineWise\static'
ALLOWED_EXTENSIONS = set([
    'txt',
    'pdf',
    'png',
    'jpg',
    'jpeg',
    'gif',
    ])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS


# Connect to Database and create database session

engine = create_engine('sqlite:///new-cuisinewise.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

username = ''


# Create anti-forgery state token

@app.route('/login')
def getLoginState():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print login_session['state']
    return state


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print 'inside gconnect'
    print login_session['state']

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        print 'state error'
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    print code

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                             scope='')
        print oauth_flow.redirect_uri
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the
                                            authorization code.'), 401)
        print 'flowexchange error'
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    print 'access_token' + str(access_token)
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        print '500 error ' + str(result.get('error'))
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match
                                            given user ID."), 401)
        print 'user ids dont match'
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match
                                            app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    # Store the access token in the session for later use.
    # login_session['credentials'] = credentials
    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    print 'Before calling getUserInfo'
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if not make a new user

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    print 'Before returning'

    data = {}
    data['userid'] = login_session['email']
    data['username'] = login_session['username']

    json_data = json.dumps(data)
    return json_data


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
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


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is not None:
        print 'In gdisconnect access token is - ' + access_token
        print 'User name is: '
        print login_session['username']
        if access_token is None:
            print 'Access Token is None'
            response = make_response(json.dumps('Current user not connected.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
            % login_session['access_token']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        print 'result is '
        print result
        if result['status'] == '200':
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            response = \
                make_response(json.dumps('Successfully disconnected.'),
                              200)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:

            response = make_response(json.dumps('Failed to revoke token for
                                     given user.', 400))
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        return 'User is not logged in'


# Endpoint1 - Show all cuisines

@app.route('/')
def showCuisines():
    print 'showCuisines'
    dbcuisines = session.query(Cuisine).order_by(asc(Cuisine.name))
    dbdishes = showlatestDishesWithCuisine()
    username = login_session.get('username')
    print username
    print dbcuisines[2].name

    return render_template('cuisines.html', cuisines=dbcuisines,
                           latestdishes=dbdishes,
                           STATE=getLoginState(),
                           loggedusername=username)


def showlatestDishesWithCuisine():
    dbdishes = session.query(Dish.id.label('dish_id'),
                             Dish.name.label('dish_name'),
                             Cuisine.id.label('cuisine_id'),
                             Cuisine.name.label('cuisine_name'),
                             Dish.created_on)
    .join(Cuisine).order_by(Dish.created_on.desc()).limit(5).all()

    for dish in dbdishes:
        print dish.dish_name, dish.cuisine_name, dish.created_on
    return dbdishes


# Endpoint2 -  Show dishes specific to Cuisine/Cuisine_id

@app.route('/cuisines/<int:cuisine_id>/dish/')
def showDishes(cuisine_id):
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    dishes = session.query(Dish).filter_by(cuisine_id=cuisine_id).all()
    username = login_session.get('username')
    loginid = login_session.get('email')
    return render_template('cuisinedishes.html', items=dishes,
                           cuisine=cuisine, loggedusername=username,
                           loginid=loginid)


# Edit a restaurant

@app.route('/cuisines/<int:cuisine_id>/<int:dish_id>/edit/',
           methods=['GET', 'POST'])
def editDish(dish_id, cuisine_id):
    username = login_session.get('username')
    loginid = login_session.get('email')
    if request.method == 'POST':
        print str(request)
        cuisine = session.query(Cuisine).filter_by
        (name=request.form['cuisine']).one()
        mydish = session.query(Dish).filter_by(id=dish_id).one()
        timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mydish.name = request.form['name']
        mydish.description = request.form['description']
        mydish.cuisine_id = cuisine.id
        mydish.recipe = request.form['recipe']
        mydish.modified_on = timenow
        session.add(mydish)
        session.commit()
        flash('%s Item Successfully Updated' % mydish.name)
        return redirect(url_for('showDishes', cuisine_id=cuisine.id,
                        loggedusername=username))
    else:
        cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
        dish = session.query(Dish).filter_by(id=dish_id).one()
        cuisineall = session.query(Cuisine.name).all()
        return render_template('editDishItem.html', dish=dish,
                               cuisine=cuisine, cuisines=cuisineall,
                               loggedusername=username)


@app.route('/cuisines/<int:cuisine_id>/<int:dish_id>/editdesc/',
           methods=['GET', 'POST'])
def editDishDesc(dish_id, cuisine_id):
    username = login_session.get('username')
    loginid = login_session.get('email')
    if request.method == 'POST':
        print str(request)
        cuisine = session.query(Cuisine).filter_by
        (name=request.form['cuisine']).one()
        mydish = session.query(Dish).filter_by(id=dish_id).one()
        timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mydish.name = request.form['name']
        mydish.description = request.form['description']
        mydish.cuisine_id = cuisine.id
        mydish.recipe = request.form['recipe']
        mydish.modified_on = timenow
        session.add(mydish)
        session.commit()
        flash('%s Item Successfully Updated' % mydish.name)
        return redirect(url_for('showDescription',
                        cuisine_id=cuisine.id, dish_id=mydish.id,
                        loggedusername=username))
    else:
        cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
        dish = session.query(Dish).filter_by(id=dish_id).one()
        cuisineall = session.query(Cuisine.name).all()
        return render_template('editDishItem.html', dish=dish,
                               cuisine=cuisine, cuisines=cuisineall,
                               loggedusername=username)


# Create a new menu item

@app.route('/restaurant/dish/new/', methods=['GET', 'POST'])
def newDish():
    username = login_session.get('username')
    loginid = login_session.get('email')

    # return render_template('addnewdish.html')

    if request.method == 'POST':
        cuisine = session.query(Cuisine).filter_by
        (name=request.form['cuisine']).one()
        timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newItem = Dish(
            name=request.form['name'],
            picurl='',
            description=request.form['description'],
            cuisine_id=cuisine.id,
            recipe=request.form['recipe'],
            created_on=timenow,
            modified_on=timenow,
            user_id=loginid,
            )
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % newItem.name)
        return redirect(url_for('showDishes', cuisine_id=cuisine.id,
                        loggedusername=username))
    else:
        cuisineall = session.query(Cuisine.name).all()
        return render_template('addnewdish.html', cuisines=cuisineall,
                               loggedusername=username)


# Delete a dish

@app.route('/restaurant/<int:dish_id>/delete', methods=['GET', 'POST'])
def deleteDish(dish_id):
    username = login_session.get('username')
    loginid = login_session.get('email')
    dish = session.query(Dish).filter_by(id=dish_id).one()
    name = dish.name
    if request.method == 'POST':
        session.delete(dish)
        session.commit()
        flash(' %s dish Successfully deleted' % name)
        return redirect(url_for('showDishes',
                        cuisine_id=dish.cuisine_id,
                        loggedusername=username))
    else:
        return render_template('deletemenuitem.html', dish=dish,
                               cuisine_id=dish.cuisine_id,
                               loggedusername=username)


# Show dish description

@app.route('/restaurant/<int:cuisine_id>/dish/<int:dish_id>/',
           methods=['GET', 'POST'])
def showDescription(dish_id, cuisine_id):
    username = login_session.get('username')
    loginid = login_session.get('email')
    cuisine = session.query(Cuisine).filter_by(id=cuisine_id).one()
    dish = session.query(Dish).filter_by(id=dish_id).one()
    return render_template('description.html', dish=dish,
                           cuisine=cuisine, loggedusername=username,
                           loginid=loginid)


@app.route('/cuisines/JSON')
def cuisinesJSON():
    restaurants = session.query(Cuisine).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/dishes/JSON')
def dishesJSON():
    cuisines = session.query(Dish).all()
    return jsonify(restaurants=[r.serialize for r in cuisines])


@app.route('/latestDishes/JSON')
def showlatestDishesWithCuisineJSON():

    cuisines = session.query(Dish.name).order_by(Dish.created_on.desc())
    for c in cuisines:
        print c

    return jsonify(Cuisines=[r.serialize for r in
                   session.query(Dish).order_by(Dish.created_on.desc())])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
