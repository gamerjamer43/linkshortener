# blueprint for the frontend routes of the application
# this file handles the main page and URL shortening functionality

from typing import Any, Literal
from flask import Blueprint, Response, render_template, jsonify, request
from ..ext import mongo, limiter
from ..domains import validate

main: Blueprint = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")

@main.route("/shorten", methods=["POST"])
@limiter.limit("3 per 30 seconds")
def shorten_url() -> tuple[Response, Literal[400]] | Response:
    data: Any = request.get_json()
    link: str = data.get("url")
    ending: str = data.get("ending")

    if not link or not ending:
        return jsonify({"error": "URL and ending are required"}), 400

    # clean link, check if its a tuple
    clean: tuple | Response = validate(link, ending)
    if isinstance(clean, tuple) and type(clean[0]) == str:
        link, ending = clean

    else:
        return clean  # if its not a tuple give an error response
    
    # also make sure it's not already in the db, no overwrites
    if mongo.db.urls.find_one({"ending": ending}):
        return jsonify({"error": "That ending is already in use"}), 400

    # cannot seem to figure out how to properly type this one
    mongo.db.urls.insert_one({"link": link, "ending": ending}) # type: ignore[union-attr]

    # return shortened link
    shortened: str = f"http://{request.host}/{ending}"
    return jsonify({"shortened_url": shortened})