# redirection routes for the backend application
# this file handles the redirection logic and trusted domain checks

from flask import Blueprint, redirect, render_template, abort
from datetime import datetime, timezone
from ..domains import trusted
from ..ext import mongo

redir: Blueprint = Blueprint("redirects", __name__)

@redir.route("/<path:ending>", methods=["GET"])
def lookup(ending):
    # pull record from db, confirm it actually exists and 404 if not
    record: str = mongo.db.urls.find_one({"ending": ending})
    if not record:
        abort(404, "URL not found")

    # check if expired
    if "expires" in record and datetime.now(timezone.utc) > record["expires"]:
        mongo.db.urls.delete_one({"ending": ending})
        abort(410, "URL has expired")

    # if its trusted, just redirect, add a no-ref header
    target = record["link"]
    if trusted(target):
        resp = redirect(target)
        resp.headers["Referrer-Policy"] = "no-referrer"
        return resp
    
    else:
        # otherwise warn about untrusted
        return render_template("warning.html", target=target, ending=ending)

@redir.route("/proceed/<path:ending>", methods=["GET"])
def proceed(ending):
    # pull record from db 
    record: str = mongo.db.urls.find_one({"ending": ending})

    # if not there 404
    if not record:
        abort(404, "URL not found")

    # otherwise just redirect
    return redirect(record["link"])