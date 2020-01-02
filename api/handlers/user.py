from flask import Blueprint, request
from flask_orator import jsonify
# from flask_jwt_extended import jwt_required

from api.store import user as user_store

user_api = Blueprint("user_api", __name__)


@user_api.route("/users/<int:user_id>", methods=["GET"])
# @jwt_required
def get_user(user_id: int):
    """Get User
    Get info about a user by id.
    ---
    parameters:
        - name: user_id
            in: path
            type: string
            required: true
    responses:
        200:
            description: A User
        404:
            description: User not found
    """
    return jsonify(user_store.get_user(user_id=user_id))


@user_api.route("/users", methods=["GET"])
# @jwt_required
def list_users():
    """List Users
    List all active users in the system.
    ---
    responses:
        200:
            description: A list of Users
    """
    return {
        "users": user_store.list_users(
            page=request.args.get("page"),
            page_size=request.args.get("page_size")
        ).serialize()
    }


@user_api.route("/users", methods=["POST"])
# @jwt_required
def create_user():
    """Create User
    Create and return a new user.
    ---
    responses:
        200:
            description: A list of Users
    """
    # TODO: Catch errors like user already exists
    return jsonify(user_store.create_user(**request.get_json())), 201
