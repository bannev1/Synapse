from flask import jsonify, request
import traceback

from app.routes.routes import Routes
from app.models import RequestGraph
from app.util.routes import checkStructure
from app.exceptions import RequestBodyException

search = Routes().search


@search.post('/nodePath')
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
		body = checkStructure(SAMPLE_REQUEST_DATA, request.get_json())
	except RequestBodyException as e: # If error with parsing data then return error
		print(traceback.format_exc())
		return jsonify({
				'status': 'error',
				'message': e
			}), 422 # Unprocessable entity status code

	print('Finding path of node...\n')

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

		print('Successfully found path!\n')

		# Return found path
		return jsonify({
				'status': 'success',
				'path': path
			}), 200

	except Exception as e: # If error encountered
		print(traceback.print_exc())
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 500
