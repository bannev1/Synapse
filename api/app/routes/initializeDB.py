from flask import jsonify
import os

from app.routes.routes import Routes
from app.models import Database


index = Routes().index


# Initialize DB tables via route
@index.get('/initialize')
def initialize() -> None:
	INDEX_FILE_LOCATION = 'app/sql/index.sql'
	indexPath = os.path.join(os.getcwd(), INDEX_FILE_LOCATION)

	db = Database()

	# Run index.sql file
	try:
		with open(indexPath, "r") as file:
			db.modify(file.read())

	# Don't close app if error
	except Exception as e:
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 500
	
	# If modified, return success
	return jsonify({
		'status': 'success'
	}), 200
