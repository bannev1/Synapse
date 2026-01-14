from flask import request, jsonify
import json

from app.routes.routes import Routes

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
	try:
		body = json.loads(request.data)
	except Exception as e: # If error with parsing data then return error
		return jsonify({
				'status': 'error',
				'message': f'Failed to construct graph – body of request contains an error. Received exception {e}.'
			}), 422 # Unprocessable entity status code
