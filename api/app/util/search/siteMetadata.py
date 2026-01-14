# Code using 3rd party to get a site's location or other relevant data

import requests
from config import Config



def siteLocation(url: str) -> str:
	"""
	Return a website's location given a URL using the IP2Location.io API

	:param url: Website URL to get location of	
	"""

	requestURL = f""