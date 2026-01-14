# Code using 3rd party to get a site's location or other relevant data

import requests

from app.util.search.siteCategorySess import SiteCategorySess
from config import Config
from app.exceptions import FailedSearchException



def siteLocation(url: str) -> str:
	"""
	Return a website's location given a domain using the IP2Location.io API 
	_(Gets the domain's admin location)_

	:param url: Website URL to get location of
	"""

	requestURL = f"https://api.ip2whois.io/v2?key={Config.IP2_API_KEY}&domain={url}"

	# Make request
	try:
		req = requests.get(requestURL)
	except:
		raise FailedSearchException(f"Request to IP2Geolocation for {url} failed")

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedSearchException(f"IP2Geolocation for {url} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	return jsonData['admin']['country']



def siteMedium(url: str) -> str:
	"""
	Return a website's medium given a url using the SiteCategory.com API

	:param url: Website URL to get location of
	"""

	# Get key
	sessKey = SiteCategorySess().key

	# Remove https and / from URL (only get base)
	url = url.replace('https', '').replace('http', '').replace('://', '')
	url = url[:url.find('/') if url.find('/') > 0 else len(url)] # Get rid of anything past the first /
	while '/' in url: # Remove all / in URL until no more
		url = url.replace('/', '')

	# URL to make request to
	requestURL = f"https://api.sitecategory.com/api/categorize"

	headers = { # Request headers
		"Authorization": f"Bearer {sessKey}",
		"Content-Type": "application/json"
	}

	formData = { # Request body data (in JSON format)
		"domain": url
	}

	# Make request
	try:
		req = requests.post(requestURL, headers=headers, json=formData)
	except:
		raise FailedSearchException(f"Request to SiteCategory for {url} failed")

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		# See if need new token
		try:
			if req.json()['error'] == 'Invalid or expired session token':
				sessKey = SiteCategorySess().generateNewKey()

				# Make request again
				req = requests.post(requestURL, headers=headers, json=formData)

				# See if valid
				if not (200 <= req.status_code < 300):
					raise Exception() # Trigger the except block
			else:
				raise Exception() # Trigger except block
		except:
			raise FailedSearchException(f"SiteCategory.com for {url} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	return jsonData['category']




def siteTitle(url: str) -> str:
	"""
	Get title given a url
	"""


