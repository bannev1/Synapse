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
