from flask import jsonify, request
import traceback

from app.routes.routes import Routes
from app.models import RequestGraph
from app.util.routes import checkStructure
from app.exceptions import RequestBodyException

search = Routes().search


@search.route('/nodePath')
def nodePath() -> None:
	"""
	Given a graph and a SourceNode's ID, find its path
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

	# Find path of node
	try:
		# Use RequestGraph
		graph = RequestGraph(body['graph'])

		# Find path of graph recursively
		path = graph.nodePath(body['source'])

		# Check if found path
		if path == None:
			return jsonify({
					'status': 'error',
					'message': 'Path not found'
				}), 500

		# Return found path
		return jsonify({
				'status': 'success',
				'path': path
			}), 200

	except Exception as e: # If error encountered
		print(traceback.print_exc())
		return jsonify({
				'status': 'error',
				'message': e
			}), 500
