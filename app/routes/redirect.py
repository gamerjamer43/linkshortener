# redirection routes for the backend application
# this file handles the redirection logic and trusted domain checks

from flask import Blueprint, redirect, render_template, abort
from ..ext import mongo
from ..domains import trusted

redirect: Blueprint = Blueprint("redirects", __name__)

@redirect.route("/<path:ending>", methods=["GET"])
def lookup(ending):
    # pull record from db, confirm it actually exists and 404 if not
    record: str = mongo.db.urls.find_one({"ending": ending})
    if not record:
        abort(404, "URL not found")

    # if its trusted, just redirect
    target = record["link"]
    if trusted(target):
        return redirect(target)
    
    else:
        # warn about untrusted
        return render_template("warning.html", target=target, ending=ending)

@redirect.route("/proceed/<path:ending>", methods=["GET"])
def proceed(ending):
    # pull record from db 
    record: str = mongo.db.urls.find_one({"ending": ending})

    # if not there 404
    if not record:
        abort(404, "URL not found")

    # otherwise just redirect
    return redirect(record["link"])
