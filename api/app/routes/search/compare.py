from flask import jsonify, request
import traceback

from app.routes.routes import Routes
from app.util.graph import CompareGraph
from app.util.routes import checkStructure
from app.exceptions import RequestBodyException

search = Routes().search


@search.post('/compare')
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

		"graph2": {
			"name": "Graph #2 Name",
			"type": "topical | locational | medium",
			"depth": 6,
			"topics": ["topic A", "topic B", "topic C"],
			"sources": [
				{
					"id": "https://bbc.com/",
					"source": "https://bbc.com/",
					"name": "BBC News Subpage",
					"sourceName": "BBC News",
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
		body = checkStructure(SAMPLE_REQUEST_DATA, request.get_json())
	except RequestBodyException as e: # If error with parsing data then return error
		print(traceback.format_exc())
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 422 # Unprocessable entity status code

	print('Creating compare graph...\n')

	# Create compare graph
	try:
		graph = CompareGraph(body['graph1'], body['graph2'])
		parsedGraph = graph.parse()
		
	except Exception as e:
		print(traceback.format_exc())
		return jsonify({
			'status': 'error',
			'message': f'Encountered an unexpected error when comparing these graphs: {e}'
		}), 500
	
	print('Successfully created compare graph!\n')

	# Return graph
	return jsonify({
		'status': 'success',
		'graph': parsedGraph
	}), 200
