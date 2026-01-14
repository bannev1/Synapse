# Custom Exceptions

class FailedGoogleSearchException(Exception):
	"""Failed Google Search Exception"""

class FailedIP2GeolocationException(Exception):
	"""Failed IP2Geolocation Exception"""

class FailedSiteCategoryException(Exception):
	"""Failed SiteCategory Exception"""

class FailedSiteCategorySessionKeyException(Exception):
	"""Failed SiteCategory Session Key Generation Exception"""

class FailedWikipediaException(Exception):
	"""Failed Wikipedia API Exception"""

class RequestBodyException(Exception):
	"""Failed to parse body of request Exception"""

class GraphConstructionException(Exception):
	"""Failed to construct graph Exception"""

class GraphParseException(Exception):
	"""Failed to parse graph Exception"""
