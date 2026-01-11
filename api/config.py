from os import getenv

class Config:
	DATABASE_URL = getenv('DATABASE_URL', '')

	GOOGLE_API_KEY = getenv('GOOGLE_API_KEY', '')
	IP2_API_KEY = getenv('IP2_API_KEY', '')
	IPINFO_API_KEY = getenv('IPINFO_API_KEY', '')
