# the new driver class

from app import create_app
from app.config import Config

app = create_app(config_object=Config)

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])