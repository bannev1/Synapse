# Code using 3rd party to get a site's location or other relevant data

import requests
import socket
from config import Config
from app.exceptions import FailedIP2GeolocationException, FailedIPInfoException



def siteLocation(url: str) -> str:
	"""
	Return a website's location given a domain using the IP2Location.io API 
	_(Gets the domain's admin location)_

	:param url: Website URL to get location of
	"""

	requestURL = f"https://api.ip2whois.io/v2?key={Config.IP2_API_KEY}&domain={url}"

	# Make request
	req = requests.get(requestURL)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedIP2GeolocationException(f"IP2Geolocation for {url} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	return jsonData['admin']['country']



def siteMedium(url: str) -> str:
	"""
	Return a website's medium given a url using the SiteCategory.com API

	:param url: Website URL to get location of
	"""

	# Remove https and / from URL (only get base)
	url = url.replace('https', '').replace('http', '').replace('://', '')
	url = url[:url.find('/') if url.find('/') > 0 else len(url)] # Get rid of anything past the first /
	while '/' in url: # Remove all / in URL until no more
		url = url.replace('/', '')

	# Get IP of domain
	url = socket.gethostbyname(url)

	requestURL = f"https://ipinfo.io/{url}"

	headers = {
		"Authorization": f"Bearer {Config.IPINFO_API_KEY}"
	}

	# Make request
	req = requests.get(requestURL, headers=headers)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedIPInfoException(f"IPInfo for {url} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	return jsonData['admin']['country']
