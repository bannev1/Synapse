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

	# Default Amount of SourceNodes per topic for diff graphs
	AMT_RESULTS_TOPICAL = 6
	AMT_RESULTS_LOCATIONAL = 6
	AMT_RESULTS_MEDIUM = 12 # This is total amt to generate initially

	# Enable Cache
	ENABLE_CACHE = True

	# Unwanted Topics
	UNWANTED_TOPICS = ['See also', 'References', 'Further reading', 'External links']
 