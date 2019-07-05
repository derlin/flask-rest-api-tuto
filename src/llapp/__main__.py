from flask.cli import FlaskGroup
from llapp import create_app

if __name__ == "__main__":
    FlaskGroup(create_app=create_app)()
