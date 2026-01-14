from os import getenv

class Config:
	# Database Connection String
	DATABASE_URL = getenv('DATABASE_URL', '')


	# 3rd Party API Keys
	GOOGLE_API_KEY = getenv('GOOGLE_API_KEY', '')
	IP2_API_KEY = getenv('IP2_API_KEY', '')
	IPINFO_API_KEY = getenv('IPINFO_API_KEY', '')


	# Google Search Engine IDs
	GOOGLE_ANY_ENGINE_ID = getenv('GOOGLE_ANY_ENGINE_ID', '')


	# Custom Configuration
	SEARCH_SITES = [ # Sites to search from
		['https://www.wikipedia.com/', 'Wikipedia'],
		["https://www.nytimes.com/", 'New York Times'],
		["https://www.youtube.com", 'YouTube'],
		["https://www.bbc.com/", 'BBC News'],
		["https://www.researchgate.net/", 'ResearchGate'],
		["https://medium.com/", 'Medium'],
		["https://arxiv.org/", 'ArXiv'],
		["https://edition.cnn.com/", 'CNN'],
		["https://www.ft.com/", 'Financial Times'],
		["https://www.sciencedirect.com/", 'ScienceDirect'],
		["https://www.britannica.com/", 'Britannica'],
	]
