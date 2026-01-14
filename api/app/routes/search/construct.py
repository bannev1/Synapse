from flask import request, jsonify

from app.exceptions import RequestBodyException
from app.routes.routes import Routes
from app.util.routes import checkStructure

search = Routes().search


@search.get('/construct')
def construct() -> None:
	SAMPLE_REQUEST_DATA = {
		'query': 'My Query/Topic',
		'sites': [
			'https://www.website1.com',
			'https://www.website2.com',
		],
		'type': 'topical | medium | locational',
		'depth': 5
	}

	# Parse request
	try:
		body = checkStructure(request.data, SAMPLE_REQUEST_DATA)
	except RequestBodyException as e: # If error with parsing data then return error
		return jsonify({
				'status': 'error',
				'message': e
			}), 422 # Unprocessable entity status code

	# 
