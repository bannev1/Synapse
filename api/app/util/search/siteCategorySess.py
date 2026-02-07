import requests

from app.exceptions import FailedSearchException
from dotenv import set_key
from config import Config


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
			# Check if already has a previous session key
			if Config.SITECATEGORY_SESSION_KEY != '':
				self.key = Config.SITECATEGORY_SESSION_KEY
			else:
				# Otherwise generate new key
				self.key = self.generateNewKey()


	def generateNewKey(self) -> str:
		"""Get a session key from SiteCategory.com"""

		url = f'https://api.sitecategory.com/api/session'

		req = requests.post(url)

		if not (200 <= req.status_code < 300): # Check to make sure didn't fail
			raise FailedSearchException(f"Failed to generate SiteCategory.com session key with status code {req.status_code}. Instead received: {req.json()}")

		# Get key
		key = req.json()['token']

		# Save key
		set_key('.env', 'SYNAPSE_SITECATEGORY_SESSION_KEY', key)
		self.key = key

		return key
