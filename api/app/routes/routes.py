from flask import Blueprint, Flask
from flask_cors import CORS


class Routes:
	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of the class is created (Singleton)."""
		
		if not cls._instance:
			cls._instance = super(Routes, cls).__new__(cls, *args, **kwargs)
		
		return cls._instance
	

	def __init__(self) -> None:
		"""Initialize the Routes class if it doesn't already exist."""
		
		if not hasattr(self, "index"):
			self.index = Flask(__name__)

			# Set up CORS
			# CORS(self.index, resources={r"/*": {"origins": [
			# 	"http://localhost:3000", # local frontend
			# 	"http://127.0.0.1:3000"  # local frontend
			# ]
			# }}, supports_credentials=True)

			# Load configuration
			self.index.config.from_object('config.Config')

			# Set up blueprints
			self.search = Blueprint('search', __name__, url_prefix='/search') # Search Route
			self.share = Blueprint('share', __name__, url_prefix='/share') # Share Route


	def registerBlueprints(self) -> None:
		"""Register blueprints once defined"""
		self.index.register_blueprint(self.search)
		self.index.register_blueprint(self.share)

		print('Configured URL Map:')
		print(self.index.url_map)

