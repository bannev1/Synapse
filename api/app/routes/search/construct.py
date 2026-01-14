from flask import request, jsonify

from app.exceptions import RequestBodyException
from app.routes.routes import Routes
from app.util.routes import checkStructure
from app.models import Graph
from app.util.graph import LocationalGraph, MediumGraph, TopicalGraph


search = Routes().search


@search.get('/construct')
def construct() -> Graph:
	"""
	Construct a graph
	"""

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

	# Get data from request body
	query = body['query']
	sites = body['sites']
	graphType = body['type']
	depth = body['depth']

	graph: Graph = None # Graph to save graph in

	# Check type of graph
	match graphType:
		case 'topical':
			graph = TopicalGraph(query, depth, sites)
			
		case 'medium':
			graph = MediumGraph(query, depth, sites)

		case 'locational':
			graph = LocationalGraph(query, depth, sites)

		# If none of those, then return error
		case _:
			return jsonify({
					'status': 'error',
					'message': f'"{graphType}" is an invalid graph type.'
				}), 422
	
	