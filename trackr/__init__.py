import os
from flask import Flask
from trackr.db import db
from flask_migrate import Migrate
from trackr import items

def create_app(test_config = None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config = True)
	app.config.from_mapping(
		SECRET_KEY = "dev",
		SQLALCHEMY_DATABASE_URI = os.path.join(app.instance_path, "trackr.sqlite"),
    )
	
	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile("config.py", silent = True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)
	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# db
	db.init_app(app)
	migrate = Migrate()
	migrate.init_app(app, db)
	
	# bp
	app.register_blueprint(items.bp)
	app.add_url_rule("/", endpoint = "index")
	
	return app
	