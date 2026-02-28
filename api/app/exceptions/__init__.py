# Custom Exceptions

class FailedSearchException(Exception):
	"""Failed to make API request"""

class RequestBodyException(Exception):
	"""Failed to parse body of request Exception"""

class GraphConstructionException(Exception):
	"""Failed to construct graph Exception"""

class GraphParseException(Exception):
	"""Failed to parse graph Exception"""

class GraphNotFound(Exception):
	"""Failed to find graph in database"""

class UnavailableLink(Exception):
	"""Failed to open link"""
