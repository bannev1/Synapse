# File for search functions
import requests

from config import Config
from app.exceptions import FailedGoogleSearchException



# Parse Google Search
def google(query: str, amtResults: int = 10, engineID: str = Config.GOOGLE_ANY_ENGINE_ID, params: str = '') -> list[dict[str]]:
	"""
	Google Search a query with a given amt of returned results
	
	:param query: Search query
	:param amtResults: Amount of returned results
	:params params: Additional parameters or config for the GET request
	:return: Parsed results, example format below:
	```
	[
		{
			'Source': 'https://www.website.com/',
			'Title': 'Website Title'
		},
		...
	]
	```

	:rtype: list[dict[str]]
	"""
	
	url = f"https://www.googleapis.com/customsearch/v1?key={Config.GOOGLE_API_KEY}&cx={engineID}&q={query}&num={amtResults}" + f"&{params}" if len(params) > 0 else ''

	# Make request
	req = requests.get(url)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedGoogleSearchException(f"Google Search Query of {query} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	# Get query data
	data = jsonData['items']

	parsedData = [] # To store parsed data

	for item in data:
		parsedData.append({
			'Source': item['url'],
			'Title': item['title']
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
		'https://www.website1.com': [
			{
				'Source': 'https://www.website1.com/',
				'Title': 'Website Title'
			},
			...
		],

		'https://www.website2.com': ...
	}
	```

	:rtype: dict[dict[str]]
	"""

	# To store queried results
	sitesResults = {}

	# Google Search each given site
	for site in sites:
		siteParam = f'SiteSearch={site}'
		parsedData = google(query, 1, params=siteParam)

		if len(parsedData) == 0: # If no results then go to next site
			continue

		# Save result
		sitesResults[site] = parsedData[0] # Only return first

	# Return results
	return sitesResults




# Google Search by Locations
def googleLocation(query: str, locations: list[str], amtResults: int = 5) -> list[str]:
	"""
	Google search with grouping by specific locations
	
	:param query: Search query
	:param locations: List of country codes to search for (see https://developers.google.com/custom-search/docs/json_api_reference#country-codes for list of country codes)
	:param amtResults: Amount of returned results per location
	:return: Parsed search results + websites, example format below:
	```
	{
		'fr': [ # France
			{
				'Source': 'https://www.website1.com/',
				'Title': 'Website Title'
			},
			...
		],

		'us': ... # United States
	}
	```

	:rtype: dict[dict[str]]
	"""

	# To store parsed data
	locationSearch = {}

	# Search each location
	for location in locations:
		locationParam = f'gl={location}'
		locationResults = google(query, amtResults, params=locationParam)

		# Save data/results
		locationSearch[location] = locationResults

	return locationSearch
