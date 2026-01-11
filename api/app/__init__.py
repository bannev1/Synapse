from flask import Flask
from flask_cors import CORS
from app.models.database import Database


def createApp():
	app = Flask(__name__)

	# Set up CORS
	CORS(app, resources={r"/*": {"origins": [
		"http://localhost:3000", # local frontend
		"http://127.0.0.1:3000"  # local frontend
	]
	}}, supports_credentials=True)

	# Load configuration
	app.config.from_object('config.Config')

	# Register blueprints (modularized routes)
	from routes import main_bp, auth_bp
	app.register_blueprint(main_bp)
	app.register_blueprint(auth_bp)

	# Close database connections on app teardown
	@app.teardown_appcontext
	def shutdown_session(exception=None):
		db = Database()
		db.close_all_connections()

	return app
