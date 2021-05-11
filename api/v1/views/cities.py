#!/usr/bin/python3
""" new view for State objects """
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def allcities(state_id):
    """ GET all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    c_list = state.cities
    res = []
    for i in c_list:
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def getcity(city_id):
    """ GET a city object """
    if city_id is None:
        abort(404)
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    return jsonify(c.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletecity(city_id=None):
    """ DELETE a city """
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    else:
        storage.delete(c)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createcity():
    """ CREATE a city """
    c = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if c is None:
        abort(400, "Not a Json")
    elif state is None:
        abort(404)
    elif "name" not in c.keys():
        abort(400, "Missing name")
    else:
        new_c = City(**c)
        storage.new(new_c)
        storage.save()
        return jsonify(new_c.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updatecity(city_id):
    """ update city with PUT """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    c = request.get_json(silent=True)
    if c is None:
        abort(400, "Not a JSON")
    for key, value in c.items():
        list_ignore = ["id", "state_id", "created_at", "updated_at"]
        if key not in list_ignore:
            setattr(obj, key, value)
            # setting attribute to be what's passed in
    obj.save()
    return jsonify(obj.to_dict()), 200
