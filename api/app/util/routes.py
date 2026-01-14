# Functions related to requests made in routes
import json
import copy

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
	
	# Check the structure of the data (deepcopy so don't accidentally pass reference)
	checkStructure(structure, copy.deepcopy(content))

	# Return value
	return content


def checkStructure(structure: dict[str], content: dict[str]) -> dict[str]:
	"""
	Recursive helper function to check the structure
	"""

	# If given dictionary
	if type(content) == dict:
		# Check against example structure to see if fits
		for key, value in structure.items():
			try: # Try to access item
				content[key]
			except:
				raise RequestBodyException(f'Missing {key} parameter in body.')
			
			# If structure's value is a list or a dictionary then iteratively check that
			if type(value) == dict or type(value) == list:
				if type(value) == type(content[key]): # Check to make sure same data type
					checkStructure(value, content[key])
				else:
					raise RequestBodyException(f'Wrong data type at {key} for value of data. Expected {type(value)}')

	# If given list
	elif type(content) == list:
		check = value[0] # Only compare first value
		
