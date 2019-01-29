# contain the application factory
# tell Python that this directory should  be treated as a package

import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # create the Flask instance
    # __name__ of the current module, to set up paths
    # the configuration files are relative to instance folder located outside the package
    # can hold local data such as configuration secrets and the database file
    app = Flask(__name__, instance_relative_config=True)

    # set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # override if exists in the instance folder, e.x. SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        # test file
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # ensure the path exist
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello!'

    from . import db
    db.init_app(app)

    from . import auth
    # import and register the blueprint
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    # no url_prefix but /
    # associate the endpoint name with url
    app.add_url_rule('/', endpoint='index')

    return app
