# basic config class, will be expanded on for production
# this is used in the wsgi.py file to create the app with the correct config

# load .env
from dotenv import load_dotenv
from os import getenv
load_dotenv()

class Config:
    # get them form env
    MONGO_URI = getenv("MONGO_URI")
    HOST = getenv("HOST")
    PORT = getenv("PORT")

    # confirm they all there
    if not MONGO_URI: raise ValueError("you have to define where your database lives at bruh. update .env with this")
    if not HOST: raise ValueError("you OBVIOUSLY have to give a host dipshit! update .env with this")
    if not PORT: raise ValueError("you have to define a port to host on. update .env with this")

    # set to false in prod obviously dipshit
    DEBUG = True