from flask import Blueprint, jsonify, make_response

index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET"])
def welcome():
    return jsonify({"msg": "Welcome!"})


@index_bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return make_response("", 204)
