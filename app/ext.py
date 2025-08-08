# extensions module for the app. a place to put all external libs so it doesn't ugly up the code
# for rn its just mongo but there will be more

from flask_pymongo import PyMongo

mongo: PyMongo = PyMongo()