from flask import jsonify, request
import traceback

from app.routes.routes import Routes
from app.util.graph import CompareGraph
from app.util.routes import checkStructure
from app.exceptions import RequestBodyException

search = Routes().search


@search.route('/nodeAdd')
def nodeAdd() -> None:
	"""
	Function to add a node given an existing graph
	"""

	SAMPLE_REQUEST_DATA = {
		"graph": {
			"name": "Graph #1 Name",
			"type": "topical | locational | medium",
			"depth": 6,
			"topics": ["topic 1", "topic 2", "topic 3"],
			"sources": [
				{
					"id": "https://nytimes.com/",
					"source": "https://nytimes.com/",
					"name": "New York Times Subpage",
					"sourceName": "New York Times",
					"topics": ['topic 1', 'topic 2'],
					"medium": "News",
					"location": "US",
					"neighbors": ["https://wikipedia.com", "https://bbc.com"]
				}
			],
			"topicLinks": [{
				"target": "node1",
				"source": "node2"
			}],
			"sourceLinks": [{
				"target": "node1",
				"source": "node2"
			}]
		},

		"source": "https://website.com"
	}

	# Parse request
	try:
		body = checkStructure(request.data, SAMPLE_REQUEST_DATA)
	except RequestBodyException as e: # If error with parsing data then return error
		print(traceback.format_exc())
		return jsonify({
				'status': 'error',
				'message': e
			}), 422 # Unprocessable entity status code
	