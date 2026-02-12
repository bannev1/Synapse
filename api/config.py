from dotenv import get_key

class Config:
	# ===================
	# CONNECTION/API KEYS
	# ===================

	# Database Connection String
	DATABASE_URL = get_key('.env', 'SYNAPSE_DATABASE_URL') or ''

	# 3rd Party API Keys
	SERPAPI_KEY = get_key('.env', 'SYNAPSE_SERPAPI_KEY') or ''
	IP_WHO_API_KEY = get_key('.env', 'SYNAPSE_IP_WHO_API_KEY') or ''
	SITECATEGORY_SESSION_KEY = get_key('.env', 'SYNAPSE_SITECATEGORY_SESSION_KEY') or ''


	# ==============
	# GENERAL CONFIG
	# ==============

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

	# Enable Cache
	ENABLE_CACHE = True

	# Unwanted Topics
	UNWANTED_TOPICS = ['See also', 'References', 'Further reading', 'External links']

	# Default Locations for locational search
	DEFAULT_LOCATIONS = ['United States', 'United Kingdom', 'Canada', 'China', 'Germany']

	# Max Subsites
	MAX_SUBSITES = 5
