# Functions related to requests made in routes
import json

from app.exceptions import RequestBodyException


def parseRequest(request, structure: dict[str] = {}) -> None:
	"""
	Function to parse request and easily access items with example structure
	"""

	# Try to load data as json
	try:
		content = json.loads(request)
	except:
		raise RequestBodyException('Failed to parse body of request as JSON.')


def checkStructure(structure: dict[str], request: dict[str]) -> dict[str]:
	"""
	Recursive helper function to check the structure
	"""

	# Check against example structure to see if fits
	for key in structure.keys():
		try: # Try to access item
			content[key]
		except:
			raise RequestBodyException(f'Missing {key} parameter in body.')