import os

from flask import Flask

def create_app(test_config=None):
    #creates and configures app
    # name is current module. Used to set up additional paths.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'travel.sqlite')
    )

    if test_config is None:
        # loads the instance configuration when not testing

        app.config.from_pyfile('config.py', silent=True)
    else:
        #loads test if config is passed in
        app.config.from_mapping(test_config)

    # ensures that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # decorator is used to establish route. in this instance http://127.0.0.1:5000/hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

# import and register DB and blueprints here
    from . import db
    db.init_app(app)

    from . import home
    app.register_blueprint(home.bp)

    from . import auth
    app.register_blueprint(auth.bp)


    return app

