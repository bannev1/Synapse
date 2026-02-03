from flask import request, jsonify
import traceback

from app.exceptions import RequestBodyException, GraphConstructionException, GraphParseException, FailedSearchException, GraphNotFound
from app.routes.routes import Routes
from app.models import Graph, CacheGraph
from app.util.routes import checkStructure
from app.util.graph import LocationalGraph, MediumGraph, TopicalGraph
from config import Config


search = Routes().search


@search.get('/')
def construct() -> Graph:
	"""
	Construct a graph
	"""

	SAMPLE_REQUEST_DATA = {
		'query': 'My Query/Topic',
		'type': 'topical | medium | locational',
		'depth': 5
	}

	# Parse request
	try:
		body = checkStructure(SAMPLE_REQUEST_DATA, request.get_json())

		# Check if list of sites is in body
		if 'sites' not in body.keys():
			body['sites'] = []
	except RequestBodyException as e: # If error with parsing data then return error
		print(traceback.format_exc())
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

	# Check if exists in Cache
	try:
		if not Config.ENABLE_CACHE: # Check if Cache enabled
			raise GraphNotFound()
		
		# Find CacheGraph
		graph = CacheGraph(query, graphType, depth, sites)
		
	except GraphNotFound:
		# Construct Graph
		try:
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
						}), 400
				
			# Return graph (parsed)
			return jsonify({
					'status': 'success',
					"graph": graph.parse()
				}), 200
		
		# If caught an error during construction
		except GraphConstructionException as e:
			print(traceback.format_exc())
			return jsonify({
					'status': 'error',
					'message': f'Failed to construct graph: {e}'
				}), 500
		
		# If caught an error while parsing graph
		except GraphParseException as e:
			print(traceback.format_exc())
			return jsonify({
					'status': 'error',
					'message': f'Failed to parse graph: {e}'
				}), 500
		
		# If error from making request
		except FailedSearchException as e:
			print(traceback.format_exc())
			return jsonify({
					'status': 'error',
					'message': f'Failed to make request for site: {e}'
				}), 500
		
		# Otherwise
		except Exception as e:
			print(traceback.format_exc())
			return jsonify({
				'status': 'error',
				'message': f'Caught unknown exception upon constructon of graph: {e}'
			})


	# Check to make sure graph exists
	if graph == None:
		return jsonify({
			'status': 'error',
			'message': 'Failed to produce graph for unknown reason.'
		}), 500

	
	# Return graph
	parsedGraph = graph.parse()

	return jsonify({
		'status': 'success',
		'graph': parsedGraph
	}), 200
