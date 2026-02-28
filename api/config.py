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

	# Enable Cache
	ENABLE_CACHE = True

	# Enable Medium
	ENABLE_MEDIUM = True

	# Unwanted Topics
	UNWANTED_TOPICS = ['See also', 'References', 'Further reading', 'External links', 'Introduction', 'Notes', 'Bibliography']

	# Default Locations for locational search
	DEFAULT_LOCATIONS = ['United States', 'United Kingdom', 'Canada', 'China', 'Germany']

	# Max Starting Nodes
	MAX_STARTING_NODES = 3

	# Max Subsites
	MAX_SUBSITES = 3

	# Max Topics (for topical)
	MAX_TOPICS = 5
