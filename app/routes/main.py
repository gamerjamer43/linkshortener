# blueprint for the frontend routes of the application
# this file handles the main page and URL shortening functionality

from typing import Any, Literal
from flask import Blueprint, Response, render_template, jsonify, request, current_app
from ..ext import mongo
from ..domains import validate

main: Blueprint = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")

@main.route("/shorten", methods=["POST"])
def shorten_url() -> tuple[Response, Literal[400]] | Response:
    data: Any = request.get_json()
    link: str = data.get("url")
    ending: str = data.get("ending")

    if not link or not ending:
        return jsonify({"error": "URL and ending are required"}), 400

    # clean link 
    clean: tuple | Response = validate(link, ending)
    if isinstance(clean, tuple):
        link, ending = clean

    else:
        return clean  # an error response

    mongo.db.urls.insert_one({"link": link, "ending": ending})
    shortened: str = f"http://{request.host}/{ending}"
    return jsonify({"shortened_url": shortened})
