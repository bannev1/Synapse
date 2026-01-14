import requests
from bs4 import BeautifulSoup, SoupStrainer

from exceptions import FailedSearchException


def subsites(url: str) -> list[str]:
	"""
	Gets the sub-urls within a url (the urls referenced/cited)
	"""

	try:
		# Get URL contents
		page = requests.get(url)
	except:
		raise FailedSearchException(f'Failed to retrieve contents of {url}.')
	
	links = []
	
	# Parse page for hyperlinks
	for link in BeautifulSoup(page, 'html.parser', parse_only = SoupStrainer('a')):
		if link.has_attr('href'):
			links.append(link)
