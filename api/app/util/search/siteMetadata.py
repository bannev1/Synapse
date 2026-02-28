# Code using 3rd party to get a site's location or other relevant data

import requests
import socket
from bs4 import BeautifulSoup
import tldextract

from config import Config
from app.util.search.siteCategorySess import SiteCategorySess
from app.exceptions import FailedSearchException



def siteLocationAndName(url: str) -> str:
	"""
	Return a website's location and source/organization name given a domain using the https://ipwho.org API 
	_(Gets the domain's admin location/registered organization name)_

	:param url: Website URL to get location/source name of
	"""

	# Remove https and / from URL (only get base)
	strippedUrl = url.replace('https', '').replace('http', '').replace('://', '')
	strippedUrl = strippedUrl[:strippedUrl.find('/') if strippedUrl.find('/') > 0 else len(strippedUrl)] # Get rid of anything past the first /
	strippedUrl = strippedUrl[:strippedUrl.find('?') if strippedUrl.find('?') > 0 else len(strippedUrl)] # Get rid of anything past the first ?
	while '/' in strippedUrl: # Remove all / in URL until no more
		strippedUrl = strippedUrl.replace('/', '')
	
	# Get domain IP
	try:
		ip = socket.gethostbyname(strippedUrl)
	
	# If failed to get hostname
	except socket.gaierror:
		# Manually get SourceName by domain
		sourceName = tldextract.extract(url).domain

		return {
			'location': 'Unknown', # Unknown
			'sourceName': sourceName.capitalize() # Make sure it's capitalized
		}


	# Configure API (with IP from socket)
	requestURL = f'https://api.ipwho.org/ip/{ip}?apiKey={Config.IP_WHO_API_KEY}'

	# Make request
	try:
		req = requests.get(requestURL)
		websiteInfo = req.json()

		# Check if went well
		if websiteInfo['success'] != True:
			# See if IP error
			if websiteInfo['message'] == 'Reserved range/Invalid IP address': # Not possible to retrieve
				# Manually get SourceName by domain
				sourceName = tldextract.extract(url).domain

				return {
					'location': 'Unknown', # Unknown
					'sourceName': sourceName.capitalize() # Make sure it's capitalized
				}
			
			# Otherwise raise error for debugging
			else:
				raise Exception(req.text)
		
		if not (200 <= req.status_code < 300):
			raise Exception(req.text) # Trigger exception block
	except Exception as e:
		raise FailedSearchException(f"Request to IPwho.org for {strippedUrl} at {ip} failed with response {e}")

	return {
			'location': websiteInfo['data']['geoLocation']['country'],
			'sourceName': websiteInfo['data']['connection']['org']
		}



def siteMedium(url: str) -> str:
	"""
	Return a website's medium given a url using the SiteCategory.com API

	:param url: Website URL to get location of
	"""

	# Check if medium needed
	if not Config.ENABLE_MEDIUM:
		return 'Unknown'

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
			if (req.json()['error'] == 'Invalid or expired session token') or (req.status_code == 401):
				sessKey = SiteCategorySess().generateNewKey()
				
				headers = { # Request headers
					"Authorization": f"Bearer {sessKey}",
					"Content-Type": "application/json"
				}

				# Make request again
				req = requests.post(requestURL, headers=headers, json=formData)

				# See if valid
				if not (200 <= req.status_code < 300):
					raise Exception(req.text) # Trigger the except block
			else:
				raise Exception(req.text) # Trigger except block
		except Exception as e:
			raise FailedSearchException(f"SiteCategory.com for {url} failed, request returned {req.status_code} status code and error {e}")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	# Check if categorized
	if ('error' in jsonData.keys()): # See if error exists first as key
		if jsonData['error'] == 'uncategorized':
			return 'Unknown'
		else:
			# Otherwise raise error
			raise FailedSearchException(f'SiteCategory.com for {url} failed with error, received {req.text}')

	return jsonData['category']




def siteTitle(url: str) -> str:
	"""
	Get title given a url
	"""

	# Try searching
	try:
		page = requests.get(url).raw
		soup = BeautifulSoup(page, 'html.parser') # Parse response
	except Exception as e:
		raise FailedSearchException(f'Failed to reach {url}, error: {str(e)}')

	# Try getting title
	try:
		return soup.find('title').string # Return title
	except AttributeError:
		# If error, then get title from domain
		title = tldextract.extract(url).domain

		return title
