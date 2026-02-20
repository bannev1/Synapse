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


def checkStructure(structure: dict[str], content: dict[str], path: str = "") -> dict[str]:
	"""
	Recursive helper function to check the structure
	"""

	if isinstance(content, dict):
		for key, value in structure.items():
			full_key = f"{path}.{key}" if path else key
			if key not in content:
				raise RequestBodyException(f'Missing {full_key} parameter in body.')
			
			if type(value) != type(content[key]):
				raise RequestBodyException(f'Wrong data type for {full_key}. Expected {type(value).__name__}')
			
			if isinstance(value, (dict, list)):
				checkStructure(value, content[key], full_key)

	elif isinstance(content, list):
		if len(structure) == 0:
			return  # Allow empty list template, no further type checking
		
		check = structure[0]
		check_type = type(check)
		
		for i, item in enumerate(content):
			item_path = f"{path}[{i}]"
			if type(item) != check_type:
				raise RequestBodyException(f'Wrong data type for {item_path}. Expected {check_type.__name__}')
			
			if isinstance(check, (dict, list)):
				checkStructure(check, item, item_path)
	
	return content
