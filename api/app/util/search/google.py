# File for search functions
import requests

from config import Config
from app.exceptions import FailedSearchException



# Parse Google Search
def google(query: str, params: str = '') -> list[dict[str]]:
	"""
	Google Search a query with a given amt of returned results using the SerpAPI
	
	:param query: Search query
	:params params: Additional parameters or config for the GET request
	:return: Parsed results, example format below:
	```
	[
		{
			'Link': 'https://www.platform123.com/',
			'Title': 'Website Title About Topic',
			'Source': 'Platform 123'
		},
		...
	]
	```

	:rtype: list[dict[str]]
	"""
	
	url = f"https://serpapi.api/search.json?api_key={Config.SERPAPI_KEY}&q={query}&hl=en" + (f"&{params}" if len(params) > 0 else '')

	# Make request
	req = requests.get(url)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedSearchException(f"Google Search Query of {query} failed, request returned {req.status_code} status code and the following: {req.text}")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	# Get query data
	data = jsonData['organic_results']

	parsedData = [] # To store parsed data

	for item in data:
		parsedData.append({
			'Link': item['link'],
			'Title': item['title'],
			'Source': item['source'] # Website Name
		})

	return parsedData



# Google Search by Specific Sites
def googleSites(query: str, sites: list[str]) -> dict[dict[str]]:
	"""
	Google search for only specific sites
	
	:param query: Search query
	:return: Parsed search results + websites, example format below:
	```
	{
		'https://www.platform123.com': [
			{
				'Link': 'https://www.platform123.com/subpage.html',
				'Title': 'Website Title About Topic',
				'Source': 'Platform 123'
			},
			...
		],

		'https://www.website.com': ...
	}
	```

	:rtype: dict[dict[str]]
	"""

	# To store queried results
	sitesResults = {}

	# Google Search each given site
	for site in sites:
		siteParam = f'SiteSearch={site}'
		parsedData = google(query, params=siteParam)

		if len(parsedData) == 0: # If no results then go to next site
			continue

	# Return results
	return sitesResults




# Google Search by Locations
def googleLocation(query: str, locations: list[str] = Config.DEFAULT_LOCATIONS) -> list[str]:
	"""
	Google search with grouping by specific locations
	
	:param query: Search query
	:param locations: List of countrys to search for
	:return: Parsed search results + websites, example format below:
	```
	{
		'Canada': [
			{
				'Link': 'https://www.platform123.com/',
				'Title': 'Website Title About Topic',
				'Source': 'Platform 123'
			},
			...
		],

		'United States': ...
	}
	```

	:rtype: dict[dict[str]]
	"""

	# To store parsed data
	locationSearch = {}

	# Search each location
	for location in locations:
		locationParam = f'location={location.replace(' ', '+')}'
		locationResults = google(query, params=locationParam)

		# Save data/results
		locationSearch[location] = locationResults

	return locationSearch
