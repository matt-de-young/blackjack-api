from flask import Blueprint, request
from flask_orator import jsonify
# from flask_jwt_extended import jwt_required

from api.store import game as game_store

game_api = Blueprint("game_api", __name__)


@game_api.route("/games/<int:game_id>", methods=["GET"])
# @jwt_required
def get_game(game_id: int):
    """Get game
    Get info about a Game by id.
    ---
    parameters:
        - name: game_id
            in: path
            type: string
            required: true
    responses:
        200:
            description: A Game
        404:
            description: Game not found
    """
    return jsonify(game_store.get_game(game_id=game_id))


@game_api.route("/games", methods=["POST"])
# @jwt_required
def create_game():
    """Create game
    Create and return a new game.
    ---
    responses:
        200:
            description: A list of games
    """
    # TODO: Catch errors like game already exists
    return jsonify(game_store.create_game(**request.get_json())), 201
