from flask import Blueprint, Flask


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

			self.search = Blueprint('search', __name__, url_prefix='/search') # Search Route
			self.share = Blueprint('share', __name__, url_prefix='/share') # Share Route

			self.index.register_blueprint(self.search)
			self.index.register_blueprint(self.share)


# Initialize Routes
Routes()
