from flask import Blueprint


class Routes:
	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of the class is created (Singleton)."""
		
		if not cls._instance:
			cls._instance = super(Routes, cls).__new__(cls, *args, **kwargs)
		
		return cls._instance
	

	def __init__(self) -> None:
		"""Initialize the Routes class if it doesn't already exist."""
		
		if not hasattr(self, "search"):
			self.search = Blueprint('search', __name__) # Search Route
			self.share = Blueprint('share', __name__) # Share Route
