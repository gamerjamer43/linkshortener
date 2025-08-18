from json import load
from pathlib import Path
from typing import Dict
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

# Load error messages when blueprint is imported
error_file = Path(__file__).parent.parent / 'errors.json'
with open(error_file, 'r') as f:
    ERRORS: Dict[int, Dict[str, str]] = {int(k): v for k, v in load(f).items()}

def register(app):
    @app.errorhandler(400)
    @app.errorhandler(401) 
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(429)
    @app.errorhandler(500)
    @app.errorhandler(502)
    @app.errorhandler(503)
    def handle_error(error):
        code = getattr(error, 'code', 500)
        info = ERRORS.get(code, {
            "title": "Unknown Error",
            "description": "An error occurred. Please try again."
        })
        
        return render_template('error.html',
                             code=code,
                             title=info["title"],
                             description=info["description"]), code