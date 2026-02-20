from flask import jsonify

from app.routes.routes import Routes
from app.models import SavedGraph
from app.exceptions import GraphNotFound

share = Routes().share


@share.get('/<str:id>')
def get(id: str) -> None:
	"""
	Get a graph saved in the local database given its ID
	"""
	
	try:
		# Retrieve and parse graph
		graph = SavedGraph(id)

		return jsonify({
			"status": "success",
			"graph": graph.parse()
		}), 200
	
	# If graph not found then return error
	except GraphNotFound:
		return jsonify({
			"status": "error",
			"message": f"Graph for {id} not found in database"
		}), 404
