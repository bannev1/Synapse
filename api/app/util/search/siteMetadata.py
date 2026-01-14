# Code using 3rd party to get a site's location or other relevant data

import requests
from config import Config
from app.exceptions import FailedIP2GeolocationException



def siteLocation(url: str) -> str:
	"""
	Return a website's location given a domain using the IP2Location.io API 
	_(Gets the domain's admin location)_

	:param url: Website URL to get location of
	"""

	requestURL = f"https://api.ip2whois.io/v2?key={Config.IP2_API_KEY}&domain={url}"

	# Make request
	req = requests.get(url)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedIP2GeolocationException(f"IP2Geolocation for {url} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	return jsonData['admin']['country']