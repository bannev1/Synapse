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



	# GENERAL CONFIG

	# Colors
	COLORS = [ # HEX code
		'#ff8a10',
		'#50b2c0',
		'#93c47d',
		'#9542f5',
		'#f54542',
		'#f542e3',
		"#abad23"
	]

	# Default Amount of SourceNodes per topic for diff graphs
	AMT_RESULTS_TOPICAL = 6
	AMT_RESULTS_LOCATIONAL = 6
	AMT_RESULTS_MEDIUM = 12 # This is total amt to generate initially
