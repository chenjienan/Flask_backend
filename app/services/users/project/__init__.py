import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(script_info=None):
    # init app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # instantiate the db
    db.init_app(app) 

    # register blueprint    
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    # register the app and db to the shell. Now we can work with 
    # the application context and the database without having to 
    # import them directly into the shell
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db }
    

    return app
