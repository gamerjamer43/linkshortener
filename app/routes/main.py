# blueprint for the frontend routes of the application
# this file handles the main page and URL shortening functionality

from flask import Blueprint, Response, jsonify, render_template, request
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from ..domains import validate
from ..ext import limiter, mongo

main: Blueprint = Blueprint("main", __name__)

# helper map to convert durations to timedeltas:
durations: dict = {
    "10min": timedelta(minutes=10), "30min": timedelta(minutes=30), # minute options
    "1hr": timedelta(hours=1), "3hr": timedelta(hours=3), "6hr": timedelta(hours=6), "12hr": timedelta(hours=12), # hour options
    "1d": timedelta(days=1), "3d": timedelta(days=3), # day options
    "1w": timedelta(weeks=1), # week options (only one frn)
}

@main.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")

@main.route("/shorten", methods=["POST"])
@limiter.limit("3 per 30 seconds")
def shorten_url() -> tuple[Response, Literal[400]] | Response:
    data: Any = request.get_json()
    link: str = data.get("url")
    ending: str = data.get("ending")
    duration: str = data.get("duration")

    if not link or not ending:
        return jsonify({"error": "URL and ending are required"}), 400

    # clean link, check if its a tuple
    clean: tuple | Response = validate(link, ending)
    if isinstance(clean, tuple) and type(clean[0]) == str:
        link, ending = clean

    else:
        return clean  # if its not a tuple give an error response
    
    # also make sure it's not already in the db, no overwrites
    if mongo.db.urls.find_one({"ending": ending}): # type: ignore[union-attr]
        return jsonify({"error": "That ending is already in use"}), 400

    # cannot seem to figure out how to properly type this one. precreate doc
    doc: dict = {"link": link, "ending": ending}

    # check for temp link duration and tag it properly with the created time
    if duration is not None and duration in durations:
        print(datetime.now(timezone.utc))
        doc.update({"duration": duration, "expires": datetime.now(timezone.utc) + durations[duration]})

    # THEN insert the doc
    mongo.db.urls.insert_one(doc) # type: ignore[union-attr]

    # return shortened link
    shortened: str = f"http://{request.host}/{ending}"
    return jsonify({"shortened_url": shortened})