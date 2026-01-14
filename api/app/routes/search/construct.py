from flask import request, jsonify

from app.exceptions import RequestBodyException
from app.routes.routes import Routes
from app.util.routes import 

search = Routes().search


"""
Route Request Structure:
{
	'query': 'My Query/Topic',
	'sites': [
		'https://www.website1.com',
		'https://www.website2.com',
		...
	],
	'type': 'topical' | 'medium' | 'locational',
	'depth': 5
}
"""


@search.get('/construct')
def construct() -> None:
	# Parse request
	try:
		body = ParseRequest(request.data)
	except RequestBodyException as e: # If error with parsing data then return error
		return jsonify({
				'status': 'error',
				'message': e
			}), 422 # Unprocessable entity status code

	# Ensure correct datastructure
