import requests
from bs4 import BeautifulSoup, SoupStrainer


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
	strippedURL = strippedURL[:strippedURL.find('?') if strippedURL.find('?') > 0 else len(strippedURL)] # Get rid of anything past the first ?
	while '/' in strippedURL: # Remove all / in URL until no more
		strippedURL = strippedURL.replace('/', '')
	
	# Return empty list for PDFs
	if '.pdf' in url:
		return []

	# Parse page for hyperlinks
	for link in BeautifulSoup(page.content, 'html.parser', parse_only = SoupStrainer('a')):
		# Make sure not breached subsites limit
		if maxSubsites >= 0 and len(links) >= maxSubsites:
			break # Break for loop

		# Otherwise get valid link only
		if link.has_attr('href'):
			sublink = link['href']

			if sublink.startswith('https://'):
				# Make sure to not add links from the same domain
				strippedLink = sublink.replace('https', '').replace('://', '')
				strippedLink = strippedLink[:strippedLink.find('/') if strippedLink.find('/') > 0 else len(strippedLink)] # Get rid of anything past the first /
				strippedLink = strippedLink[:strippedLink.find('?') if strippedLink.find('?') > 0 else len(strippedLink)] # Get rid of anything past the first ?
				while '/' in strippedLink: # Remove all / in URL until no more
					strippedLink = strippedLink.replace('/', '')

				# Check equivalence
				if strippedLink.strip().lower() != strippedURL.strip().lower():
					links.append(sublink)


	return links
