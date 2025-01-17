#!/usr/bin/python3
""" create a variable app_views which is an instance of Blueprint """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """ returns status: OK """
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """ create endpoint that retrieves the number of eachobjects by type """
    return jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)})
