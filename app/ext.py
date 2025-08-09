# extensions module for the app. a place to put all external libs so it doesn't ugly up the code
# for rn its just mongo and limiter but there will be more

from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

from flask_pymongo import PyMongo

mongo: PyMongo = PyMongo()
limiter: Limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour", "1 per second"]
)