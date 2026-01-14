# File for search functions
import requests

from config import Config
from app.exceptions import FailedGoogleSearchException



# Parse Google Search
def google(query, amtResults = 10, engineID = Config.GOOGLE_ANY_ENGINE_ID, params: str = '') -> list[dict[str]]:
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
def googleSites(query, sites, amtResults = 1) -> dict[list[dict[str]]]:
	"""
	Google search for only specific sites
	
	:param query: Search query
	:param amtResults: Amount of returned results per website
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

	:rtype: dict[list[dict[str]]]
	"""

	# To store queried results
	sitesResults = {}

	# Google Search each given site
	for site in sites:
		siteParam = f'SiteSearch={site}'
		parsedData = google(query, amtResults, params=siteParam)

		# Save result
		sitesResults[site] = parsedData

	# Return results
	return sitesResults
