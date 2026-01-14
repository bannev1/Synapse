# File for search functions
import requests

from config import Config
from app.exceptions import FailedGoogleSearchException


# Parse Google Search
def google(query, amtResults = 10) -> list[str]:
	ENGINE_ID = "4454355756a844f0e" # From Google Search API docs
	
	url = f"https://www.googleapis.com/customsearch/v1?key={Config.GOOGLE_API_KEY}&cx={ENGINE_ID}&q={query}&amt={amtResults}"

	# Make request
	req = requests.get(url)

	# Check to ensure went well (check via status code)
	if not (200 <= req.status_code < 300):
		raise FailedGoogleSearchException(f"Google Search Query of {query} failed, request returned {req.status_code} status code")
	
	# Otherwise parse the JSON response
	jsonData = req.json()

	# Get query data
	data = jsonData['queries']