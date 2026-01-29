from flask import jsonify, request

from app.routes.routes import Routes
from app.util.graph import CompareGraph
from app.util.routes import checkStructure
from app.exceptions import RequestBodyException

search = Routes().search


@search.route('/compare')
def compare() -> None:
	"""
	Create a compare graph given two graphs
	"""

	SAMPLE_REQUEST_DATA = {
		"graph1": {
			"name": "Graph #1 Name",
			"type": "topical | locational | medium",
			"depth": 6,
			"topics": ["topic 1", "topic 2", "topic 3"],
			"sources": [
				{
					"id": "https://nytimes.com/",
					"source": "https://nytimes.com/",
					"name": "New York Times",
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

		"graph2": {
			"name": "Graph #2 Name",
			"type": "topical | locational | medium",
			"depth": 6,
			"topics": ["topic A", "topic B", "topic C"],
			"sources": [
				{
					"id": "https://bbc.com/",
					"source": "https://bbc.com/",
					"name": "BBC News",
					"topics": ['topic A', 'topic B'],
					"medium": "News",
					"location": "US",
					"neighbors": ["https://nytimes.com", "https://bbc.com"]
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
		body = checkStructure(request.data, SAMPLE_REQUEST_DATA)
	except RequestBodyException as e: # If error with parsing data then return error
		return jsonify({
				'status': 'error',
				'message': e
			}), 422 # Unprocessable entity status code

	# Create compare graph
	try:
		graph = CompareGraph(body['graph1'], body['graph2'])
	except Exception as e:
		return jsonify({
			'status': 'error',
			'message': 'Encountered an unexpected error when comparing these graphs'
		}), 500
	
	# Return graph
	return jsonify({
		'status': 'success',
		'graph': graph
	}), 200
