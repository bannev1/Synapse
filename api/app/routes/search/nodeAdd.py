from flask import jsonify, request
import traceback

from app.routes.routes import Routes
from app.models import RequestGraph
from app.util.routes import checkStructure
from app.exceptions import RequestBodyException

search = Routes().search


@search.post('/nodeAdd')
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
		body = checkStructure(SAMPLE_REQUEST_DATA, request.get_json())
	
		# If graph type is topical, make sure "topic" argument exists
		if body['graph']['type'] == 'topical':
			body['topic'] # Try to get the topic
	except RequestBodyException as e: # If error with parsing data then return error
		print(traceback.format_exc())
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 422 # Unprocessable entity status code
	
	# Add node
	try:
		# Use RequestGraph
		graph = RequestGraph(body['graph'])

		# Add node depending on type of graph
		if graph.type == 'topical':
			graph.addNode(body['source'], body['topic'])

		else:
			graph.addNode(body['source'])

		# Return updated graph
		return jsonify({
				'status': 'success',
				'graph': graph.parse()
			}), 200
	
	except Exception as e:
		print(traceback.format_exc())
		return jsonify({ # Return failed as error encountered
				'status': 'error',
				'message': str(e)
			}), 500
