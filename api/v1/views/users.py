#!/usr/bin/python3
""" new view for User """

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allusers():
    """ GET all users """
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getusers(user_id):
    """ GET user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteuser(user_id=None):
    """ DELETE user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createuser():
    """ POST to create user """
    user_dict = request.get_json(silent=True)
    if user_dict is None:
        abort(400, 'Not a JSON')
    elif "email" not in user_dict.keys():
        abort(400, "Missing email")
    elif "password" not in user_dict.keys():
        abort(400, "Missing password")
    else:
        new_u = User(**user_dict)
        storage.new(new_u)
        storage.save()
        return (jsonify(new_u.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateuser(user_id):
    """ Updates a user with PUT """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    for key, value in s.items():
        list_ignore = ["id", "created_at", "updated_at"]
        if key not in list_ignore:
            setattr(obj, key, value)
            # setting attribute to be what's passed in
    obj.save()
    return jsonify(obj.to_dict()), 200
