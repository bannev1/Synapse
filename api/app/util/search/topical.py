# Code for getting topics and whatnot using the wikipedia API

import requests

from app.exceptions import FailedSearchException


# Get topics
def getTopics(query: str)-> list[str]:
	"""
	Get a list of topics given the topic/query
	
	:param query: Topic/query to get topics of
	:return: List of topics (string format)
	:rtype: list[str]
	"""

	url = f'https://en.wikipedia.org/w/api.php?action=parse&page={query}&format=json&prop=tocdata'

	req = requests.get(url).raw

	# Check if request worked
	if not (200 <= req.status_code < 300):
		raise FailedSearchException(f"Failed Wikipedia API request for topics with status code {req.status_code} at {url}, and given response \n{req.json()}")

	# Parse data
	response = req.json()
	topics = []

	for section in response['parse']['tocdata']['sections']:
		topics.append(section['line'])

	return topics
