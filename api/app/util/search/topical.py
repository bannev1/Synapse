# Code for getting topics and whatnot using the wikipedia API

import requests
import traceback

from app.exceptions import FailedSearchException
from config import Config


# Get topics
def getTopics(query: str)-> list[str]:
	"""
	Get a list of topics given the topic/query
	
	:param query: Topic/query to get topics of
	:return: List of topics (string format)
	:rtype: list[str]
	"""

	url = f'https://en.wikipedia.org/w/api.php?action=parse&page={query}&format=json&prop=tocdata'
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
	}

	# Check if request worked
	try:
		req = requests.get(url, headers=headers)

		# Parse data
		response = req.json()
		topics = []

		for section in response['parse']['tocdata']['sections']:
			if section['line'] not in Config.UNWANTED_TOPICS:
				topics.append(section['line'])

		return topics

	except Exception as e:
		print(traceback.format_exc())

		raise FailedSearchException(f"Failed Wikipedia API request for topics, error {e}")
