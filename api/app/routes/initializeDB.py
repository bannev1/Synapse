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
	conn = db.get_connection()
	
	try:
		cursor = conn.cursor()
		cursor.execute(open(indexPath, "r").read())
		cursor.close()
	
	# Don't close app if error
	except Exception as e:
		return jsonify({'Error': str(e)})
	
	# Release connection
	finally:
		db.release_connection(conn)
