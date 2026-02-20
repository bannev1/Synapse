from flask import request, jsonify
import traceback

from app.exceptions import RequestBodyException
from app.routes.routes import Routes
from app.util.routes import checkStructure
from app.models import SavedGraph, RequestGraph

share = Routes().share


@share.route('/save/<id>', methods=["UPDATE"])
def save(id: str) -> None:
	"""
	Update an existing/stored graph at ID with a new graph
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
		}
	}

	# Parse request
	try:
		body = checkStructure(SAMPLE_REQUEST_DATA, request.get_json())
	except RequestBodyException as e: # If error with parsing data then return error
		print(traceback.format_exc())
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 422 # Unprocessable entity status code

	# Upload to create a saved graph
	try:
		# Parse new graph
		newGraph = RequestGraph(body['graph'])

		# Update saved graph
		SavedGraph.updateByID(id, newGraph)

		return jsonify({
				'status': 'success'
			}), 200

	except Exception as e:
		print(traceback.format_exc())
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 500
	