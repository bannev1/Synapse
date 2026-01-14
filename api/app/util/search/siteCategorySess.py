import requests


class SiteCategorySess:
	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of the class is created (Singleton)."""
		
		if not cls._instance:
			cls._instance = super(SiteCategorySess, cls).__new__(cls, *args, **kwargs)
		
		return cls._instance
	

	def __init__(self) -> None:
		"""Class to store the SiteCategory Session Key or to generate more"""

		if not hasattr(self, "key"):
			self.generateNewKey() # Generate session key


	def generateNewKey(self) -> str:
		"""Get a session key from SiteCategory.com"""

		
