#!/usr/local/bin/python3

from flask.cli import FlaskGroup
from project import app

cli = FlaskGroup(app)

# run and manage the app from the command line
if __name__ == '__main__':
    cli()


# (env)$ export FLASK_APP=project/__init__.py
# (env)$ python manage.py run