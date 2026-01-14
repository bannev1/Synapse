# File for search functions
import requests

from config import Config
from app.exceptions import FailedGoogleSearchException


# Parse Google Search
def google(query, amtResults = 10, sites: list[str] = Config.SEARCH_SITES) -> list[dict[str]]:
	"""
	Google Search a query with a given amt of returned results (no locational restriction)
	
	:param query: Search query
	:param amtResults: Amount of returned results
	:param sites: Sites to search for (empty list for all/any sites)
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

	ENGINE_ID = Config.GOOGLE_ANY_ENGINE_ID # From Google Search API docs
	
	url = f"https://www.googleapis.com/customsearch/v1?key={Config.GOOGLE_API_KEY}&cx={ENGINE_ID}&q={query}&amt={amtResults}"

	# Make request
	req = requests.get(url)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedGoogleSearchException(f"Google Search Query of {query} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	# Get query data
	data = jsonData['items']