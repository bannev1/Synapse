import requests
from bs4 import BeautifulSoup, SoupStrainer

from config import Config

def subsites(url: str, maxSubsites: int = -1) -> list[str]:
	"""
	Gets the sub-urls within a url (the urls referenced/cited)
	"""

	try:
		# Get URL contents
		page = requests.get(url)
	except:
		return [] # Assume empty page
	
	links = []

	# Remove https and / from URL (only get base) for no host domain
	strippedURL = url.replace('https', '').replace('http', '').replace('://', '')
	strippedURL = strippedURL[:strippedURL.find('/') if strippedURL.find('/') > 0 else len(strippedURL)] # Get rid of anything past the first /
	while '/' in strippedURL: # Remove all / in URL until no more
		strippedURL = strippedURL.replace('/', '')
	
	# Parse page for hyperlinks
	for link in BeautifulSoup(page.content, 'html.parser', parse_only = SoupStrainer('a')):
		# Make sure not breached subsites limit
		if maxSubsites >= 0 and len(links) >= maxSubsites:
			break # Break for loop

		# Otherwise get link
		if link.has_attr('href') and 'https://' in link:
			# Make sure to not add links from the same domain
			strippedLink = link.replace('https', '').replace('://', '')
			strippedLink = strippedLink[:strippedLink.find('/') if strippedLink.find('/') > 0 else len(strippedLink)] # Get rid of anything past the first /
			while '/' in strippedLink: # Remove all / in URL until no more
				strippedLink = strippedLink.replace('/', '')

			# Check equivalence
			if strippedLink.strip().lower() != strippedURL.strip().lower():
				links.append(link)

		# Make sure not too many links
		if len(links) == Config.MAX_SUBSITES:
			return links


	return links
